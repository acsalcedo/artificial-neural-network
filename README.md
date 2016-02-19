# artificial-neural-network
Proyecto de Redes Neuronales - Inteligencia Artificial 2

## Para correr:

    python main.py -t <datasetType> -i <inputDataFile> -n <numHiddenLayerNeurons> -w <weightsFile> -r <learnRate> -c <fileToClassify>"

Donde:

1. Dataset type es el tipo de los datos de entrenamiento. Las opciones son las siguientes:
  1. circle
  2. iris
  3. iris con tres clases
  4. operadores lógicos
2. Input data file es el archivo de los datos de entrenamiento.
3. Num hidden layer neurons es el número de neuronas en la capa intermedia.
4. Weights file (opcional) es un archivo que ya tiene guardado los pesos de un previo entrenamiento.
  1. En el nombre de archivo se debe especificar el path a partir del directorio de pesos del tipo de datos. Por ejemplo en el caso de iris el nombre de un archivo de pesos sería:

    ``3/weights_neurons9_rate0.05_20160218145053_iris90.data``

5. Learn rate (opcional) es la tasa de aprendizaje.
6. File to classify (opcional) es el archivo de los datos a clasificar.


###Ejemplo de entrenamiento de la red:

    python main.py -t 1 -i generated2000.txt -n 5
    
###Ejemplo de clasificación del archivo testSet con un archivo de pesos ya generados:

      python main.py -t 1 -i generated2000.txt -n 2 -c testSet.txt
      -w neurons/given/weights_neurons2_rate0.05_20160217234523_datos_P1_RN_EM2016_n2000.txt 
      
###Ejemplo de la clasificación de iris con tres clases:
      
      python main.py -t 3 -i iris.data -c bezdekIris.data -n 4 -w 3/weights_neurons4_rate0.05_20160218083029_iris50.data

