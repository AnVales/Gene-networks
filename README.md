🧬 Gene-networks
📌 Descripción

Este proyecto analiza la red regulatoria de genes en E. coli a partir de un archivo de interacciones (network_tf_gene.txt) obtenido de RegulonDB
.

📂 Archivos principales

e.coli_regulatory_network_script.py → código para procesar la red.

network_tf_gene.txt → datos de relaciones factor de transcripción → gen.

🔹 Flujo del análisis
1️⃣ Input

📄 Archivo de texto con pares de regulación TF → Gene.

2️⃣ Procesamiento (Python)

⚙️ Construcción de red de interacciones.
📊 Conteo de conexiones (in/out degree).
🔎 Identificación de genes clave (hubs, reguladores principales).

3️⃣ Resultados

Número de genes reguladores y regulados.

Tamaño de la red (nodos, aristas).

Distribución de conexiones.

🔹 Ejemplo visual
TF1 ───▶ GeneA
TF1 ───▶ GeneB
TF2 ───▶ GeneC
TF3 ───▶ GeneA


🔗 Representado como un grafo dirigido:

👤 TF (factor de transcripción) → 🧬 Gen regulado

⚡ Ejecución
python e.coli_regulatory_network_script.py network_tf_gene.txt

🚀 Posibles extensiones

✨ Visualización con networkx o matplotlib.

✨ Identificación de módulos/regulons.

✨ Comparación con redes de otras bacterias.
