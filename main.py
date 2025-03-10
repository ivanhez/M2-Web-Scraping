import re
import csv

def cargar_html(ruta_archivo):
    """
    Carga el contenido HTML en un solo string.
    """
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        return f.read()

def extraer_productos(html):
    """
    Extrae el nombre de producto y la URL de imagen con la estructura:
    <div class="item--contenido-PD"> ... <p class="cort_not_h-PD ">NOMBRE</p> ... <img src="URL" ...> ... </div>
    """

    bloques = re.split(r'<div class="item--contenido-PD"\s*>', html)
    patron_nombre = re.compile(
        r'<p\s+class="cort_not_h-PD\s*"\s*>(.*?)</p>',
        re.DOTALL
    )

    patron_imagen = re.compile(
        r'<img[^>]*\ssrc="([^"]+)"[^>]*>',
        re.DOTALL
    )
    
    productos = []
    
    for bloque in bloques:
        match_nombre = patron_nombre.search(bloque)
        if not match_nombre:
            continue
        nombre_producto = match_nombre.group(1).strip()
        
        match_imagen = patron_imagen.search(bloque)
        if not match_imagen:
            continue
        url_imagen = match_imagen.group(1).strip()
        
        productos.append((nombre_producto, url_imagen))
    
    return productos

def exportar_csv(productos, archivo_salida):
    """
    Genera el archivo CSV
    """
    with open(archivo_salida, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Producto", "Imagen"])
        for nombre, url in productos:
            writer.writerow([nombre, url])

def main():
    ruta_html = "Guatemala Digital - guatemaladigital.com.html"
    
    html = cargar_html(ruta_html)
    
    productos_encontrados = extraer_productos(html)
    
    nombre_csv = "productos.csv"
    exportar_csv(productos_encontrados, nombre_csv)
    
    print(f"Se han exportado {len(productos_encontrados)} productos a '{nombre_csv}'")

if __name__ == "__main__":
    main()
