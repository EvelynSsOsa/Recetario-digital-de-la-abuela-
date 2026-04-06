from pathlib import Path
import os
import shutil
#####################def rutas() : es la base para cualquier ruta que se utilizara en la app
def rutas():
    dep_rutas = os.getcwd()# obtenemos la ruta actual con ayuda del metodo "os.getcwd()"
    ruta_rece = Path(dep_rutas,"recetario") #con "Path" tomamos a la variable "dep_rutas" y le agregamos "recetario"... dandole formato de ruta
    ruta_rece.mkdir(exist_ok=True)## decimos que si "ruta_rece" no exite cre esta ultima carpeta que mencionamos "recetario" y si, si existe continuar
    return ruta_rece  ## etsa función nos ayuda a obetenr la ruta base de donde tenemos nuestra carpeta de recetario

#################### def crear_categoria(rutas) -> esta función nos ayuda a devolver la carpeta que creo el usuario
def crear_categoria(rutas):## pasamos como parametro la ruta base
    nueva_categoria = input("Cúal va a ser el nombre de la categoria?") ## le preguntamos al usuario, cual sera el nombre de carpeta/categoria
    cate_nue = rutas/nueva_categoria##al pasar como paraemtro la ruta base, y al ser un objeto "Path", solo le agregamos la carpeta/ categoria que quiere el usuario
    cate_nue.mkdir(exist_ok=True)## con "mkdir" decimos que cre la carpeta que agregamos a la ruta base, mientras que al mismo tiempo comprabamos que exista dicha carpeta
    return cate_nue ## regresamos la categoria creada que se guardo en la variable "cate_nue"

#################### def crear_receta(ruta_categoria)-> ayudamos a crear el archvio en la categoria que el usuario ya seleciono con anterioridad
def crear_receta(ruta_categoria):## pasamos la categoria selecionada como paramtero
    nota = input("¿Cúal es el nombre de la receta?") ## tenemos un input que usaremos para darle nombre al archivo y a la receta
    recetita = []## creamos una lista vacia, que ira almacenando cada parte de la receta
    while True:## damos a entender que miestras el usuario no rompa el bucle esto continuarar
        r = input("Quieres continuar con la receta? s/n: ") ##
        if r == "s":## mientras la respuesta del usuario sea s vamos a preguntarle si quiere continuar con la receta
            receta = input("Escribe: ")## el usuario coloca su receta
            recetita.append(receta) #pasamos el input que guarda la variable "receta" como parametro de append y así poder ir agregando elementos a la lista
        else:
            print("Aquí esta tu receta: ") ## se imprime este mensaje una vez que el usuario quiere dejar de escribir su receta y nos vamos directoa return
            break## una vez la respuesta del usuario sea diferente de "s" se rompe este bucle
    receta_completa = nota +"\n"+"\n".join(recetita) ## en "receta_completa" damos fromato a como queremos que se vea nuestra receta
    receta_nueva = ruta_categoria/f"{nota}.txt"## creamos la ruta, pasamos el paraemtro que ya trae la ruta de la categoria (esta ya es un objeto path)
    ##por ultimo añadimos el input de la varibel nota, que le dara nombre al archivo
    with open (receta_nueva,"w") as archivo:## abrimos el archivo en modo escritura
         archivo.write(receta_completa)## con write, pasamos como parametro la variable que contiene el formato de receta
    return receta_nueva## receta nueva nos devuelve ya la receta tal cual la dejo el usuario

##################### def seleccionar_categoria(categoria)-> nos trae de regreso la categoria selecionada por el usuario, este metodod
##es primordial para muchas de nuestra funciones, pues nos devulve un valor fundamnetal para cualquier movimiento y manipulación de datos
def seleccionar_categoria(categorias):## pasamos como paramtero la ruta base de nuestro recetario
    ## decimos que por cada elemento que tengamos en "categorias":
    for cate in categorias.iterdir(): ##itedir()-> es un metodo iterador que recorre una a una las carpetas de un directorio
        print(cate.name)## imprimimos el nombre de dicha categoria y lo mostraremos en pantalla
    while True: ## decimos que mientras el usuario no rompa el bucle nos mantengamos dentro
        cate_selec= input("Selecciona una categoria:") ## el usuario ingresa el nombre de la categoria que quiere
        ## pasamos el objeto "Path"(parametro de esta función) y agregamos la variable que guarda el nombre de la categoria selecionada
        selecion_categoria = categorias/cate_selec
        ## "if selecion_categoria.exists() and" -> decimos que si la ruta de esta carpeta existe yyyyy ademas
        ##"and selecion_categoria.is_dir():" -> se encuentra en el directorio entonces:
        if selecion_categoria.exists() and selecion_categoria.is_dir():
            print(f"La categoria seleccionada es: {cate_selec}")## mostramos en pantalla cual fue la categoria seleccionada
            return selecion_categoria## y regresamos la ruta de lacategoria seleciiondad
        else:
            print("Esa categoria de recetas no existe, intentalo de nuevo")


#### def seleccionar_receta(cate_selec): esta función nos a UNICAMENTE SELECCIONAR una receta/archivo del directorio selecionado, que
##### de hecho en esta función el paramtero que necesitamos es la ruta de la carpeta/categoria seleccionada por el usuario:
def selecionar_receta(cate_selec):## pasamos la función de "seleccionar_categoria" que nos da la ruta donde tenemos la categoria
    recetas = [rec.name for rec in cate_selec.glob("*.txt")]
    ## tenemos una lista "recetas"-> IMPORTANTE ACLARAR QUE AQUI SOLO OBTENEMOS ARCHIVOS EN UNA LISTA POR SUFIJOS COMUNES -> txt
    if not recetas:## si aun no hay recetas dentro de esta caperta, es decir que nuestra lista este vacia
        print("Aun no has creado ninguna receta")## imprimes esto
    for rece in recetas:## decimos que por cada archivo en la lista "recetas"
        print(rece)## nos imprima el nombre del archivo de esa receta
    while True:## decimos que mietras el usuario no rompa el bucle, repetiremos la pregunta
          receta = input("¿Qué receta quieres?: ")## le pedimos al usuario que ingrese, el nombre del archivo/receta que quiere
          if f"{receta}.txt" in recetas:## decimos que receta esta dentro de la lista "recetas"
              ##pasamos el parametro "cate_selec" (objeto"Path") y le agregamos el input(receta), que contiene la receta seleccionada
              receta_lectura = cate_selec/f"{receta}.txt"## nos traiga la ruta
              return receta_lectura## devolvemos la ruta
          else:## si la receta selecionada no esta dentro de la lista "recetas":
              print("Esa receta no se encuentra en esta categoria, intentalo de nuevo. \n")


#########################def leer_receta(receta_seleccionada)-> literlamente nos abre el archivo en modo lectura y ya
def leer_receta(receta_selecionada):## aqui pasamos a la función de "selecionar_receta" que nos da la ruta del archivo que queremos leer
    with open(receta_selecionada, "r") as archivo:## esta función tiene como proposito abrir ese archivo y solo leerlo
        contenido_receta = archivo.read() ## guardamos en una variable, el metodo "read()" aplicado al archivo
    return contenido_receta## devolvemos esa misma variable


######################### def eliminar:_receta(receta_selecionada)->  su objetivo es eliminar el archivo/receta selecionada
def eliminar_receta(receta_selecionada):## aquí igual pasamos a la función de "selecionar_receta" pues nos pasa la ruta del archivo que queremos eliminar
    ## decimos que si "receta_selecionada" existe y ademas se encuentra dentro de este directorio:
     if receta_selecionada.exists() and receta_selecionada.is_file():
         receta_selecionada.unlink()## con e metodo "unlink" borramos ese archivo
         print("Tu receta a sido eliminada")## y luego imprimimos este mensaje en pantalla

     else:## en dado caso de que esa receta no exista, se imprime en pantalla:
         print("Esa receta no existe, intentalo de nuevo. \n")

############# def eliminar categoria:-> aqui tenemos como proposito eliminar una carpeta, pasamos como parametro la ruta de la categoria selecionada
def eliminar_categoria(seleciona_cate):
    ##decimos que si "seleciona_cate" existe y ademas se encuentra en el directorio base "recetario" entonces:
     if seleciona_cate.exists() and seleciona_cate.is_dir():
         ## en la variable "elimina_categoria" guardamos el metodo aplicado al paramtero "seleciona_cate"
         elimina_categoria = shutil.rmtree(seleciona_cate)
         print("tu categoria fue borrada con exito")## despues imprimimos esto en pantalla
         return elimina_categoria
     else:## en dado caso de que el paramtero no se encuentre en el directorio base:
         print("Esa categoria no existe y no se pudo eliminarinten")## imprimimos en pantalla


def limpiar_pantalla():
    os.system("clear")

while True:
  limpiar_pantalla()
  print("Hola Bienvenido a tu recetario \n ")
  print("Elige una opción: \n ")
  print("1.-Leer receta \n ")
  print("2.-Crear receta \n ")
  print("3.-Crear categoría\n ")
  print("4.-Eliminar receta \n ")
  print("5.-Eliminar categoria \n ")
  print("6.-Finalizar programa\n ")
  respuesta= input ("Con que quieres empezar?")

  if respuesta == "1":
      limpiar_pantalla()
      base = rutas()
      cat = seleccionar_categoria(base)
      recetita = selecionar_receta(cat)
      print(leer_receta(recetita))
      input("\nPresiona Enter para continuar...")

  elif respuesta == "2":
      base = rutas()
      cat = seleccionar_categoria(base)
      crear_receta(cat)
      print("Tu receta ya ha sido guardada")
      input("\nPresiona Enter para continuar...")
  elif respuesta == "3":
      base = rutas()
      crear_categoria(base)
      input("\nPresiona Enter para continuar...")
  elif respuesta == "4":
      base = rutas()
      cat = seleccionar_categoria(base)
      mostrar_recetas = selecionar_receta(cat)
      eliminar_receta(mostrar_recetas)
      input("\nPresiona Enter para continuar...")
  elif respuesta == "5":
      base = rutas()
      cat = seleccionar_categoria(base)
      eliminar_categoria(cat)
      input("\nPresiona Enter para continuar...")
  elif respuesta == "6":
      print("Adios")
      input("\nPresiona Enter para continuar...")
      break
  else:
      print("Esa opción no es valida")







