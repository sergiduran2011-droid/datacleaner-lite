import csv
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union


# ==========================================
# 1. TRATAMIENTO DE CADENAS Y ENCABEZADOS
# ==========================================

def clean_column_name(name: str) -> str:
    """
    Limpia un nombre de columna individual:
    - Normaliza caracteres (elimina acentos).
    - Convierte a minúsculas.
    - Reemplaza caracteres no alfanuméricos por '_'.
    """
    name = unicodedata.normalize('NFKD', str(name)).encode('ASCII', 'ignore').decode('utf-8')
    name = re.sub(r'[^\w]+', '_', name)
    return name.strip('_').lower()


def clean_column_names(headers: List[str]) -> List[str]:
    """
    Aplica clean_column_name a una lista de encabezados.
    Resuelve duplicados añadiendo sufijos numéricos únicos (_1, _2, etc.).
    """
    cleaned_names: List[str] = []

    for header in headers:
        base_name = clean_column_name(header) or "column"
        cleaned = base_name
        counter = 1
        
        while cleaned in cleaned_names:
            cleaned = f"{base_name}_{counter}"
            counter += 1
            
        cleaned_names.append(cleaned)

    return cleaned_names


# ==========================================
# 2. DETECCIÓN DE TIPOS Y DELIMITADORES
# ==========================================

def detect_delimiter(file_path: Union[str, Path]) -> str:
    """Detecta automáticamente el delimitador de un CSV (',', ';', '\t')."""
    path = Path(file_path)
    try:
        with open(path, newline='', encoding='utf-8') as file:
            sample = file.read(4096)
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {path}")

    if not sample:
        return ','

    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=[',', ';', '\t'])
        return dialect.delimiter
    except csv.Error:
        return ','


def infer_type(value: str) -> str:
    """Infiere el tipo de dato básico de un valor en texto."""
    v = value.strip()
    if not v:
        return "empty"
    if v.isdigit() or (v.startswith('-') and v[1:].isdigit()):
        return "int"
    try:
        float(v)
        return "float"
    except ValueError:
        pass
    if v.lower() in ("true", "false"):
        return "bool"
    return "string"


# ==========================================
# 3. INSPECCIÓN COMPLETA Y REPORTE
# ==========================================

def inspect_csv(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Inspecciona un CSV eficientemente:
    - Recuento de filas y columnas.
    - Conteo de nulos.
    - Conteo de filas 100% duplicadas.
    - Inferencia del tipo de dato predominante por columna.
    """
    path = Path(file_path)
    delimiter = detect_delimiter(path)
    total_rows = 0
    headers: List[str] = []
    null_counts: Dict[str, int] = {}
    seen_rows = set()
    duplicate_rows = 0
    type_counts: Dict[str, Dict[str, int]] = {}

    with open(path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=delimiter)
        try:
            headers = next(reader)
        except StopIteration:
            return {
                'total_rows': 0,
                'total_cols': 0,
                'null_counts': {},
                'headers': [],
                'duplicate_rows': 0,
                'column_types': {},
            }

        total_cols = len(headers)
        null_counts = {header: 0 for header in headers}
        type_counts = {header: {'int': 0, 'float': 0, 'bool': 0, 'string': 0} for header in headers}

        for row in reader:
            # Ignorar filas completamente vacías
            if not row or not any(field.strip() for field in row):
                continue

            total_rows += 1
            row_tuple = tuple(row)
            if row_tuple in seen_rows:
                duplicate_rows += 1
            else:
                seen_rows.add(row_tuple)

            for index in range(total_cols):
                val = row[index] if index < len(row) else ''
                if val is None or str(val).strip() == '':
                    null_counts[headers[index]] += 1
                else:
                    t = infer_type(val)
                    if t in type_counts[headers[index]]:
                        type_counts[headers[index]][t] += 1

    # Determinar tipo predominante por columna
    column_types = {}
    for header in headers:
        counts = type_counts[header]
        most_common = max(counts, key=counts.get) if any(counts.values()) else 'string'
        column_types[header] = most_common if counts[most_common] > 0 else 'string'

    return {
        'total_rows': total_rows,
        'total_cols': total_cols,
        'null_counts': null_counts,
        'headers': headers,
        'duplicate_rows': duplicate_rows,
        'column_types': column_types,
    }


def generate_report(file_path: Union[str, Path]) -> str:
    """Genera un informe formateado para consola con barras de progreso y métricas clave."""
    path = Path(file_path)
    metrics = inspect_csv(path)
    
    total_rows = metrics['total_rows']
    total_cols = metrics['total_cols']
    headers = metrics['headers']
    null_counts = metrics['null_counts']
    dup_rows = metrics['duplicate_rows']
    col_types = metrics['column_types']
    
    lines = []
    lines.append("=" * 70)
    lines.append(f"📊 REPORTEDATACLEANER | {path.name}")
    lines.append("=" * 70)
    lines.append(f"📁 Ruta: {path.resolve()}")
    lines.append(f"📐 Filas: {total_rows:,}  |  Columnas: {total_cols}  |  Filas duplicadas: {dup_rows:,}")
    lines.append("-" * 70)
    
    if total_cols == 0:
        lines.append("⚠️ El archivo está vacío o no contiene datos válidos.")
    else:
        lines.append(f"{'COLUMNA':<22} {'TIPO':<8} {'NULOS':>8}   {'PORCENTAJE':<15}")
        lines.append("-" * 70)
        for header in headers:
            nulls = null_counts.get(header, 0)
            pct = (nulls / total_rows * 100) if total_rows > 0 else 0.0
            ctype = col_types.get(header, 'string')
            
            filled = int(round(pct / 10))
            bar = "█" * filled + "░" * (10 - filled)
            
            header_display = header[:21]
            lines.append(f"{header_display:<22} {ctype:<8} {nulls:>8,}   {pct:>5.1f}% [{bar}]")
            
    lines.append("=" * 70)
    return "\n".join(lines)


# ==========================================
# 4. LIMPIEZA PROFUNDA Y EXPORTACIÓN
# ==========================================

def clean_file(
    input_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    remove_duplicates: bool = True,
    fill_nulls: Optional[str] = None
) -> Path:
    """
    Limpia un archivo CSV completo y lo guarda en disco:
    - Normaliza nombres de encabezados.
    - Elimina espacios blancos sobrantes en cada celda.
    - Ignora filas completamente vacías.
    - Opcional: Elimina filas idénticas duplicadas.
    - Opcional: Rellena celdas vacías con un valor por defecto.
    """
    in_path = Path(input_path)
    if output_path is None:
        out_path = in_path.parent / f"{in_path.stem}_cleaned{in_path.suffix}"
    else:
        out_path = Path(output_path)

    delimiter = detect_delimiter(in_path)

    with open(in_path, newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter=delimiter)
        try:
            raw_headers = next(reader)
        except StopIteration:
            raise ValueError("El archivo de entrada está vacío.")

        cleaned_headers = clean_column_names(raw_headers)
        
        rows_to_write = []
        seen = set()

        for row in reader:
            # Ignorar filas vacías
            if not row or not any(field.strip() for field in row):
                continue
            
            # Limpiar espacios de cada celda
            cleaned_row = [f.strip() if f.strip() else (fill_nulls if fill_nulls is not None else '') for f in row]

            # Ajustar la longitud de la fila si faltan columnas
            while len(cleaned_row) < len(cleaned_headers):
                cleaned_row.append(fill_nulls if fill_nulls is not None else '')

            row_tuple = tuple(cleaned_row)
            if remove_duplicates:
                if row_tuple in seen:
                    continue
                seen.add(row_tuple)

            rows_to_write.append(cleaned_row)

    with open(out_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(cleaned_headers)
        writer.writerows(rows_to_write)

    return out_path


# ==========================================
# 5. INTERFAZ DE LÍNEA DE COMANDOS (CLI)
# ==========================================

def main():
    """Punto de entrada de la consola (CLI)."""
    if len(sys.argv) < 2:
        print("Uso:")
        print("  datacleaner report <archivo.csv>")
        print("  datacleaner clean <archivo.csv> [-o resultado.csv]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "report":
        if len(sys.argv) < 3:
            print("Error: Indica el archivo CSV a analizar.")
            sys.exit(1)
        filepath = sys.argv[2]
        print(generate_report(filepath))

    elif command == "clean":
        if len(sys.argv) < 3:
            print("Error: Indica el archivo CSV a limpiar.")
            sys.exit(1)
        filepath = sys.argv[2]
        out_path = None
        if "-o" in sys.argv:
            idx = sys.argv.index("-o")
            if idx + 1 < len(sys.argv):
                out_path = sys.argv[idx + 1]

        result = clean_file(filepath, output_path=out_path)
        print(f"✨ Archivo limpio guardado con éxito en: {result}")

    else:
        print(f"Comando '{command}' no reconocido. Usa 'report' o 'clean'.")


if __name__ == "__main__":
    main()