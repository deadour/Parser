#importar librerias
from ply import lex 
import time
import re
import ply.lex as lex
import ply.yacc as yacc
import os
import codecs
import msvcrt
title_doc = True

##################### LEXER#################################
reservadas = ['DOCTYPE', 
              'OPEN_ARTICLE','CLOSE_ARTICLE',
              'OPEN_INFO','CLOSE_INFO',
              'OPEN_TITLE','CLOSE_TITLE',
              'OPEN_EMAIL','CLOSE_EMAIL',
              'OPEN_STREET','CLOSE_STREET',
              'OPEN_CITY','CLOSE_CITY',
              'OPEN_STATE','CLOSE_STATE',
              'OPEN_PHONE','CLOSE_PHONE',
              'OPEN_COPYRIGHT','CLOSE_COPYRIGHT',
              'OPEN_YEAR','CLOSE_YEAR',
              'OPEN_HOLDER','CLOSE_HOLDER',
              'OPEN_AUTHOR','CLOSE_AUTHOR', 
              'OPEN_DATE','CLOSE_DATE',
              'OPEN_FIRST_NAME','CLOSE_FIRST_NAME',
              'OPEN_SURNAME','CLOSE_SURNAME',
              'OPEN_SECTION','CLOSE_SECTION',
              'OPEN_SIMPLE_SECTION','CLOSE_SIMPLE_SECTION',
              'OPEN_ABSTRACT','CLOSE_ABSTRACT',
              'OPEN_PARA','CLOSE_PARA',
              'OPEN_SIMPARA','CLOSE_SIMPARA',
              'OPEN_IMPORTANT','CLOSE_IMPORTANT',
              'OPEN_COMMENT','CLOSE_COMMENT',
              'OPEN_EMPHASIS','CLOSE_EMPHASIS',
              'OPEN_MEDIA','CLOSE_MEDIA',
              'CLOSE_MEDBRAC',
              'OPEN_IMAGE_OBJECT', 'CLOSE_IMAGE_OBJECT',
              'IMAGE_DATA', 'VIDEO_DATA',
              'OPEN_VIDEO_OBJECT','CLOSE_VIDEO_OBJECT',
              'CLOSE_URL_LINK',
              'OPEN_LINK','CLOSE_LINK', 
              'OPEN_ITEMIZED_LIST','CLOSE_ITEMIZED_LIST',
              'OPEN_LIST_ITEM', 'CLOSE_LIST_ITEM',
              'OPEN_TABLE','CLOSE_TABLE',
              'OPEN_T_GROUP','CLOSE_T_GROUP',
              'OPEN_HEAD','CLOSE_HEAD',
              'OPEN_FOOT','CLOSE_FOOT',
              'OPEN_BODY','CLOSE_BODY',
              'OPEN_ROW', 'CLOSE_ROW',
              'OPEN_ENTRYTBL','CLOSE_ENTRYTBL',
              'OPEN_ENTRY','CLOSE_ENTRY',
              'OPEN_ADDRESS','CLOSE_ADDRESS',            
              'TAG_ERRONEO','CARACTER_INVALIDO', 
              'OPEN_IMAGEDATA','OPEN_VIDEO_DATA','CLOSE_VIDEO_DATA',"CLOSE_IMAGEDATA"]


title_doc = True
en_info = False
en_important = False
en_section = False

tokens= reservadas+['TEXTO', 'URL', 'CONTENT']

def t_CONTENT(t):
    r'[^<>]+'
    contenido = t.value[1:-1]
    if hasattr(t.lexer, 'content'):
        t.lexer.content += t.value
    return t
    
#definición de salto de pagina
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)
        
def t_DOCTYPE (t):
    r'<!DOCTYPE\s+article>'

    return t

def t_OPEN_ARTICLE  (t) :
    r'<article>'
    return t 

def t_CLOSE_ARTICLE (t):
    r'</article>'
    return t
  
def t_OPEN_INFO (t):
      r'<info>'
      global en_info, title_doc
      en_info = True
      title_doc = False
      return t

def t_CLOSE_INFO (t):
      r'</info>'
      global en_info, title_doc
      en_info = False
      title_doc = True
      return t
  
def t_OPEN_TITLE (t):
    r'<title>'
    if en_section:
      html.write('<h2>')
    elif title_doc:
      html.write('<h1>')
    elif en_info:
      html.write('<h3 class="info">')
    elif en_important:
      html.write('<h3 class="important">')
    else:  
      pass
    t.lexer.content = ""
    return t

def t_CLOSE_TITLE (t):
    r'</title>'
    if en_section:
        html.write(t.lexer.content.strip())
        html.write('</h2>\n')
    elif title_doc:
        html.write(t.lexer.content.strip())
        html.write('</h1>\n')
         
    elif en_info or en_important:
        html.write(t.lexer.content.strip())
        html.write('</h3>\n')
    else:
        pass
    return t

def t_OPEN_ADDRESS (t):
      r'<address>'
      return t

def t_CLOSE_ADDRESS (t):
      r'</address>'
      return t

def t_OPEN_STREET (t):
      r'<street>'
      return t

def t_CLOSE_STREET (t):
      r'</street>'
      return t

def t_OPEN_CITY (t):
      r'<city>'
      return t

def t_CLOSE_CITY (t):
      r'</city>'
      return t

def t_OPEN_STATE (t):
      r'<state>'
      return t

def t_CLOSE_STATE (t):
      r'</state>'
      return t

def t_OPEN_PHONE (t):
      r'<phone>'
      return t

def t_CLOSE_PHONE (t):
      r'</phone>'
      return t

def t_OPEN_DATE (t):
      r'<date>'
      return t

def t_CLOSE_DATE (t):
      r'</date>'
      return t

def t_OPEN_EMAIL (t):
      r'<email>'
      return t

def t_CLOSE_EMAIL (t):
      r'</email>'
      return t

def t_OPEN_AUTHOR (t):
      r'<author>'
      return t

def t_CLOSE_AUTHOR (t):
      r'</author>'
      return t

def t_OPEN_FIRST_NAME (t):
      r'<firstname>'
      return t
def t_CLOSE_FIRST_NAME (t):
      r'</firstname>'
      return t

def t_OPEN_SURNAME (t):
      r'<surname>'
      return t
def t_CLOSE_SURNAME (t):
      r'</surname>'
      return t

def t_OPEN_COPYRIGHT(t):
      r'<copyright>'
      return t

def t_CLOSE_COPYRIGHT (t):
      r'</copyright>'
      return t

def t_OPEN_YEAR (t):
      r'<year>'
      return t

def t_CLOSE_YEAR (t):
      r'</year>'
      return t

def t_OPEN_HOLDER (t):
      r'<holder>'
      return t

def t_CLOSE_HOLDER (t):
      r'</holder>'
      return t

# Hago una bandera para que me diga si es o no el título del documento en base a si está o no dentro de un section/abstract
def t_OPEN_SECTION (t):
      r'<section>'
      global title_doc, en_section
      title_doc = False
      en_section = True
      
      return t
def t_CLOSE_SECTION (t):
     r'</section>'
     global title_doc, en_section
     title_doc = True
     en_section = False
     return t

def t_OPEN_SIMPLE_SECTION (t) :
     r'<simplesection>'
     global title_doc, en_section
     title_doc = False
     en_section = True
     return (t)

def t_CLOSE_SIMPLE_SECTION (t) :
     r'</simplesection>'
     global title_doc, en_section
     title_doc = True
     en_section = False
     global bandera
     bandera = False
     return (t)

def t_OPEN_ABSTRACT (t):
      r'<abstract>'
      global title_doc, en_section
      title_doc = False
      en_section = False
      return t

def t_CLOSE_ABSTRACT (t):
      r'</abstract>'
      global title_doc, en_section
      title_doc = True
      en_section = False
      return t

def t_OPEN_PARA (t):
    r'<para>'
    if en_info:
        html.write('<p class="info">\n')
    elif en_important:
        html.write('<p class="important">\n')
    elif en_section or title_doc:
        html.write('<p>')
    else:
        pass
    t.lexer.content = ""
    return t

def t_CLOSE_PARA (t):
      r'</para>'
      if en_info or en_important or en_section or title_doc:
        html.write(t.lexer.content.strip()+'\n')
        html.write('</p>\n')
      else:
        pass
      return t

def t_OPEN_SIMPARA (t):
      r'<simpara>'
      if en_info:
        html.write('<p class="info">\n')
      elif en_important:
        html.write('<p class="important">\n')
      elif en_section or title_doc:
        html.write('<p>')
      else:
        pass
      t.lexer.content = ""
      return t

def t_CLOSE_SIMPARA (t):
      r'</simpara>'
      if en_info or en_important or en_section or title_doc:
        html.write(t.lexer.content.strip()+'\n')
        html.write('</p>\n')
      else:
        pass
      return t

def t_OPEN_IMPORTANT (t):
      r'<important>'
      global en_important, title_doc
      en_important = True
      title_doc = False
      return t

def t_CLOSE_IMPORTANT (t):
      r'</important>'
      global en_important, title_doc
      en_important = False
      title_doc = True
      return t

def t_OPEN_COMMENT (t):
      r'<comment>'
      return t

def t_CLOSE_COMMENT (t):
      r'</comment>'
      return t

def t_OPEN_EMPHASIS (t):
      r'<emphasis>'
      return t

def t_CLOSE_EMPHASIS (t):
      r'</emphasis>'
      return t

def t_CLOSE_MEDBRAC (t):
     r'/>'
     return t

def t_OPEN_MEDIA (t):
    r'<mediaobject>'  
    return t

def t_CLOSE_MEDIA (t):
     r'</mediaobject>'
     return t

def t_OPEN_IMAGE_OBJECT (t):
      r'<imageobject>'
      return t

def t_CLOSE_IMAGE_OBJECT (t):
      r'</imageobject>'
      return t

# Definición de la expresión regular para la URL de imagen
def t_OPEN_IMAGEDATA (t):
     r'<imagedata\s+fileref='
     return t
def t_CLOSE_IMAGEDATA (t):
  r'</imagedata>'
  return t
def t_IMAGE_DATA(t):
      r'"https?://[^\s<>"]+|www\.[^\s<>"]+\.(png|jpg|jpeg|gif|bmp|tiff|pdf|eps|svg)+[^\s<>"]'
      return t



def t_OPEN_VIDEO_OBJECT (t):
      r'<videoobject>'
      return t

def t_CLOSE_VIDEO_OBJECT (t):
      r'</videoobject>'
      return t

def t_OPEN_VIDEO_DATA (t):
     r'<videodata\s+fileref='
     return t

# Definición de la expresión regular para la URL de video
def t_URL(t):
    r'\"(http|https|ftp|ftps)://[^/\s:]+(:\d+)?(/[^#\s])?(\#\S)?\+["]'
    return (print (f"URL: {t.value}")) 

def t_VIDEO_DATA(t):
      r'"https?://[^\s<>"]+|www\.[^\s<>"]+\.(mp4|mov|wmv|avi|avch|flv|f4v|swf|mkv|mpeg-2)"'
      return t

def t_CLOSE_VIDEO_DATA (t):
      r'</videodata>'
      return t
#definición de tokens de cadena de URL 

def t_OPEN_LINK (t):
    r'<link\s+xlink:href\s*=\s*"[^"]*"+[>]'
    global reservadas
    reservadas.append(f"<a link href={t.value[12: -2]}>")
    return t

def t_CLOSE_LINK (t):
      r'</link>'
      return t

def t_CLOSE_URL_LINK(t):
    r'>'
    return t

def t_OPEN_ITEMIZED_LIST (t):
     r'<itemizedlist>'
     html.write('<ul>')  
     return t

def t_CLOSE_ITEMIZED_LIST (t):
     r'</itemizedlist>'
     html.write('</ul>')
     
     return t
      
def t_OPEN_LIST_ITEM (t):
  r'<listitem>'
  html.write('<li>')
  t.lexer.content = ""
  return t
     

def t_CLOSE_LIST_ITEM (t):
     r'</listitem>'
     html.write(t.lexer.content.strip())
     html.write('</li>\n')
     return t

def t_OPEN_TABLE (t):
      r'<informaltable>'
      html.write('<table>\n')
      return t

def t_CLOSE_TABLE (t):
      r'</informaltable>'
      html.write('</table>\n')
      return t

def t_OPEN_T_GROUP (t):
     r'<tgroup>'
     return t

def t_CLOSE_T_GROUP (t):
     r'</tgroup>'
     return t

def t_OPEN_HEAD (t):
     r'<thead>'
     return t

def t_CLOSE_HEAD (t):
     r'</thead>'
     return t

def t_OPEN_FOOT (t):
     r'<tfoot>'
     return t

def t_CLOSE_FOOT (t):
     r'</tfoot>'
     return t

def t_OPEN_BODY (t):
     r'<tbody>'
     return t

def t_CLOSE_BODY (t):
     r'</tbody>'
     return t

def t_CLOSE_ROW (t):
      r'</row>'
      html.write('</tr>\n')
      return t

def t_OPEN_ROW (t):
      r'<row>'
      html.write('<tr>\n')
      return t

def t_OPEN_ENTRYTBL(t):
    r'<entrytbl>'
    return t

def t_CLOSE_ENTRYTBL(t):
    r'</entrytbl>'
    return t

def t_OPEN_ENTRY (t):
      r'<entry>'
      html.write('<td>')
      t.lexer.content = ""
      return t

def t_CLOSE_ENTRY (t):
      r'</entry>'
      html.write(t.lexer.content.strip())
      html.write('</td>\n')
      return t


def t_TAB(t):
  r'\t'
  pass

def t_ESPACIO(t):
    r'\ '
    pass

def t_TEXTO(t): 
    r'[^<>]+'
    return t

# Manejo de errores, solo lo usamos debido a que sin esto, no se ejecuta
def t_error(t):  
    print("Carácter no válido: %s" % t.value[0])
    t.lexer.skip(1)

def t_CARACTER_INVALIDO(t):  # funciona como el t_error
    r'<[^>]+>'
    return print (f'Caracter no valido: {t.value}')



#--------------------------------------------------- Arranca el programa-----------------------------------

   

###################PARSER##########################

#gramaticas


def p_inicio (p):
    """inicio : DOCTYPE gen_article"""


def p_gen_article(p):
    '''gen_article : OPEN_ARTICLE gen_allart CLOSE_ARTICLE'''

   

def p_gen_allart (p) :
    ''' gen_allart : gen_info gen_titl gen_data gen_secciones
                    | gen_info  gen_data gen_secciones
                    | gen_titl gen_data gen_secciones
                    | gen_data gen_secciones
                    | gen_titl gen_data 
                    | gen_data    
                    | gen_info gen_data'''
    


def p_gen_data (p):
    """gen_data : gen_list
    | gen_important
    | gen_para
    | gen_simp
    | adr
    | mo
    | gen_table
    | gen_com
    | gen_abs
    | gen_list gen_data
    | gen_important gen_data
    | gen_para gen_data
    | gen_simp gen_data
    | adr gen_data
    | mo gen_data
    | gen_table gen_data
    | gen_com gen_data
    | gen_abs gen_data"""

def p_gen_secciones (p):
     """gen_secciones : gen_section gen_secciones
      | gen_simpsec gen_secciones
       | gen_section 
       | gen_simpsec"""
   


def p_gen_section (p):
    ''' gen_section : OPEN_SECTION gen_allart CLOSE_SECTION        
    '''


def p_gen_simpsec (p):
    ''' gen_simpsec : OPEN_SIMPLE_SECTION simpsec CLOSE_SIMPLE_SECTION'''
  

def p_simpsec (p) :
    """simpsec :  gen_info gen_titl gen_data 
                    | gen_info  gen_data  
                    | gen_data gen_secciones
                    | gen_titl gen_data 
                    | gen_data    """


def p_gen_info  (p):
    '''gen_info : OPEN_INFO info CLOSE_INFO'''


def p_info (p): 
    '''info : mo 
            | gen_abs 
            | adr 
            | gen_aut 
            | gen_date 
            | gen_copy 
            | gen_titl  
            | mo info 
            | gen_abs info 
            | adr info 
            | gen_aut info 
            | gen_date info 
            | gen_copy info 
            | gen_titl info 
    '''


def p_gen_abs (p):
    ''' gen_abs : OPEN_ABSTRACT gen_titl infoab CLOSE_ABSTRACT
        | OPEN_ABSTRACT infoab CLOSE_ABSTRACT '''
    


def p_infoab (p):
    ''' infoab : gen_para
        | gen_simp
        | gen_para infoab
        | gen_simp infoab '''
    

def p_adr (p):
    ''' adr : OPEN_ADDRESS genad CLOSE_ADDRESS
        | OPEN_ADDRESS TEXTO CLOSE_ADDRESS '''
    
def p_genad (p):### CORREGIR EN EL WORD
    ''' genad : gen_street 
        | gen_state
        | gen_city
        | gen_phone
        | gen_email
        | TEXTO
        | gen_street genad
        | gen_state genad
        | gen_city genad
        | gen_phone genad
        | gen_email genad 
        | TEXTO genad '''
    
def p_gen_aut (p):
        ''' gen_aut : OPEN_AUTHOR aut CLOSE_AUTHOR '''

def p_aut (p):
    ''' aut : gen_firstn
        | gen_surn
        | gen_firstn aut
        | gen_surn aut '''
    

def p_gen_copy (p):
    ''' gen_copy : OPEN_COPYRIGHT copy CLOSE_COPYRIGHT '''
 

def p_copy (p):
    ''' copy : gen_year
        | gen_year gen_holder '''


    
def p_gen_firstn (p):
    '''gen_firstn : OPEN_FIRST_NAME genall CLOSE_FIRST_NAME '''

def p_gen_surn (p):
    ''' gen_surn : OPEN_SURNAME genall CLOSE_SURNAME '''
   

def p_gen_street (p):
    ''' gen_street : OPEN_STREET genall CLOSE_STREET '''
   

def p_gen_city(p):
    ''' gen_city : OPEN_CITY genall CLOSE_CITY '''
    

def p_gen_state(p):
    ''' gen_state : OPEN_STATE genall CLOSE_STATE '''
   

def p_gen_phone (p):
    ''' gen_phone : OPEN_PHONE genall CLOSE_PHONE '''
    

def p_gen_email (p):
    ''' gen_email : OPEN_EMAIL genall CLOSE_EMAIL '''
   

def p_gen_date (p):
    ''' gen_date : OPEN_DATE genall CLOSE_DATE '''
    

def p_gen_year (p):
    ''' gen_year : OPEN_YEAR genall CLOSE_YEAR '''
    


def p_gen_holder (p):
    ''' gen_holder : OPEN_HOLDER genall CLOSE_HOLDER '''
    
def p_genall (p):   ### CORREGIR WORD 
    ''' genall : TEXTO
        | gen_link
        | gen_emp
        | gen_com
        | TEXTO genall
        | gen_link genall
        | gen_emp genall
        | gen_com genall '''
  
  


def p_gen_titl (p): ### CORREGIR WORD 
    ''' gen_titl : OPEN_TITLE cont_tit CLOSE_TITLE '''  
  

def p_cont_tit (p):
    ''' cont_tit : TEXTO
        | gen_emp
        | gen_link
        | gen_email
        | TEXTO cont_tit
        | gen_emp cont_tit
        | gen_email cont_tit
        | gen_link cont_tit '''


def p_gen_simp (p):### CORREGIR WORD 
    ''' gen_simp : OPEN_SIMPARA conex CLOSE_SIMPARA ''' 
 

def p_gen_emp (p):### CORREGIR WORD 
    ''' gen_emp : OPEN_EMPHASIS conex CLOSE_EMPHASIS '''    

def p_gen_link (p):
    ''' gen_link : OPEN_LINK conex CLOSE_LINK '''

def p_gen_com (p):
    ''' gen_com : OPEN_COMMENT conex CLOSE_COMMENT '''

def p_conex (p):
    ''' conex : TEXTO 
        | gen_emp
        | gen_link
        | gen_email
        | gen_aut
        | gen_com
        | gen_emp conex
        | TEXTO conex
        | gen_link conex
        | gen_email conex
        | gen_aut conex
        | gen_com conex '''
    
def p_gen_para (p):
    ''' gen_para : OPEN_PARA op_para CLOSE_PARA '''
 
def p_op_para (p):
    ''' op_para : TEXTO
        | gen_link
        | gen_emp
        | gen_email
        | gen_aut
        | gen_com
        | gen_list
        | gen_important
        | adr
        | mo
        | gen_table
        | TEXTO op_para
        | gen_link op_para 
        | gen_emp op_para
        | gen_email op_para
        | gen_aut op_para
        | gen_com op_para
        | gen_list op_para
        | gen_important op_para
        | adr op_para
        | mo op_para
        | gen_table op_para '''
    
def p_gen_important (p):### CORREGIR WORD 
    ''' gen_important : OPEN_IMPORTANT gen_titl important CLOSE_IMPORTANT
        | OPEN_IMPORTANT important CLOSE_IMPORTANT '''

def p_important (p):
    ''' important : gen_list
        | gen_important
        | gen_para
        | gen_simp
        | adr
        | mo
        | gen_table
        | gen_com
        | gen_abs
        | gen_list important
        | gen_important important
        | gen_para important
        | gen_simp important
        | adr important
        | mo important
        | gen_table important
        | gen_com important
        | gen_abs important '''
    
def p_gen_list (p):
    ''' gen_list : OPEN_ITEMIZED_LIST item CLOSE_ITEMIZED_LIST '''
    
def p_item (p):
    '''item : OPEN_LIST_ITEM newlist CLOSE_LIST_ITEM'''

def p_newlist (p):
    """newlist : gen_important
    | gen_para
    | gen_simp
    | gen_list
    | gen_table
    | mo
    | gen_com
    | gen_abs
    | gen_important newlist
    | gen_para newlist
    | gen_simp newlist
    | gen_list newlist
    | gen_table newlist
    | mo newlist
    | gen_com newlist
    | gen_abs newlist"""
   


def p_mo (p):
    ''' mo : OPEN_MEDIA j CLOSE_MEDIA '''



def p_j (p):
    ''' j : gen_info video r
        | gen_info image r
        | r '''
def p_r (p):
    ''' r : image
        | video
        | image r
        | video r '''


def p_video (p):
    ''' video : OPEN_VIDEO_OBJECT info OPEN_VIDEO_DATA VIDEO_DATA CLOSE_MEDBRAC CLOSE_VIDEO_DATA CLOSE_VIDEO_OBJECT
    | OPEN_VIDEO_OBJECT OPEN_VIDEO_DATA VIDEO_DATA CLOSE_MEDBRAC CLOSE_VIDEO_DATA CLOSE_VIDEO_OBJECT'''
   

  

def p_image (p):
    ''' image : OPEN_IMAGE_OBJECT info OPEN_IMAGEDATA IMAGE_DATA CLOSE_MEDBRAC  CLOSE_IMAGE_OBJECT
            | OPEN_IMAGE_OBJECT OPEN_IMAGEDATA IMAGE_DATA CLOSE_MEDBRAC CLOSE_IMAGEDATA CLOSE_IMAGE_OBJECT '''
    



def p_gen_listitem (p):
     """ gen_listitem : OPEN_ITEMIZED_LIST conex3 CLOSE_ITEMIZED_LIST """

def p_conex3 (p):
    """ conex3 : fin 
        | conex3 fin """

def p_fin (p) :
        """fin : gen_important
        | gen_para
        | gen_simp
        | adr
        | gen_listitem
        | mo
        | gen_table
        | gen_com
        | gen_abs
        | gen_important conex3
        | gen_para conex3
        | gen_simp conex3
        | adr conex3
        | gen_listitem conex3
        | mo conex3
        | gen_table conex3
        | gen_com conex3
        | gen_abs conex3"""

def p_gen_table (p):
    ''' gen_table : OPEN_TABLE inf_tb CLOSE_TABLE '''



def p_inf_tb (p):
    ''' inf_tb : mo
        | t_group
        | mo inf_tb
        | t_group inf_tb '''


def p_t_group (p):
    ''' t_group : OPEN_T_GROUP gen_tgroup CLOSE_T_GROUP '''
   


def p_gen_tgroup (p):
    ''' gen_tgroup : t_head t_body t_foot
        | t_body t_foot
        | t_head t_body
        | t_body '''

            
        


def p_t_head (p):
    ''' t_head : OPEN_HEAD row CLOSE_HEAD '''
   


def p_t_body (p):
    ''' t_body : OPEN_BODY row CLOSE_BODY '''
    


def p_t_foot (p):
    ''' t_foot : OPEN_FOOT row CLOSE_FOOT '''


def p_row (p):
    ''' row : OPEN_ROW entry CLOSE_ROW row
        | OPEN_ROW entry CLOSE_ROW
        | OPEN_ROW entry_tb CLOSE_ROW
        | OPEN_ROW entry_tb CLOSE_ROW row '''
 

def p_entry_tb (p):
    ''' entry_tb : OPEN_ENTRYTBL t_head t_body CLOSE_ENTRYTBL  '''
    


def p_entry (p):
    ''' entry : OPEN_ENTRY gen_entry CLOSE_ENTRY'''

def p_gen_entry (p) :
    """ gen_entry : TEXTO gen_entry
    | OPEN_ITEMIZED_LIST 
    | gen_important
    | gen_para
    | gen_simp
    | mo
    | gen_com
    | gen_abs
    | TEXTO
    | gen_listitem gen_entry
    | gen_important gen_entry
    | gen_para gen_entry
    | gen_simp gen_entry
    | mo gen_entry
    | gen_com gen_entry
    | gen_abs gen_entry
    """
errores = 0
def p_error(p):
    global errores
    if p:
        print  (f"Error de sintaxis en línea {p.lineno}. Culpable: {p.value}\n")
        errores += 1
    else:
        print ("Fin del archivo \n")


#iterativo o archivo
time.sleep (1)
print ('Tipo de carga:')
print ('A) Interactiva')
print ('B) Carga por archivo')
print ('Si desea usar los ejemplos del grupo, ingrese opcion B y ponga la direccion de la carpeta')
time.sleep (1)
rta = (input ('Ingrese la opcion\n>'))
time.sleep (1)


if rta.upper() == "A":
      print ('Escriba su texto, recuerde que si pulsa el doble ENTER se da como finalizado el texto.')
      time.sleep (1)
      info =""
      while True:
            linea = input("")
            if linea == "":
                break
            info += linea + "\n"
elif rta.upper ()=="B":  
    opcion = "z"
    print ("Por favor, ingrese por teclado la dirección de la carpeta en donde se encuentran los archivos.xml")
    directorio = input("Ingresa la dirección de archivo: ")

    # Obtener todos los archivos en el directorio
    archivos = [archivo for archivo in os.listdir(directorio) if archivo.endswith(".xml")]


    print("Archivos en la ubicación:")
    for i, archivo in enumerate(archivos, start=1):
        print(f"{i}. {archivo}")

    
    num_archivo = int(input("Ingresa el número del archivo que deseas seleccionar: "))

    # Verificar si el número es válido y guardar el archivo seleccionado en la variable info
    if 1 <= num_archivo <= len(archivos):
        nombre_archivo = archivos[num_archivo - 1]
        ruta_archivo = os.path.join(directorio, nombre_archivo)
        with open(ruta_archivo, "r") as archivo:
            info = archivo.read()



html = open(ruta_archivo.replace(".xml", ".html"), "w")
html.write('''
<html>
  <head>
    <style>
      .info {
        background-color: green;
        color: white;
      }
      .important {
        background-color: red;
        color: white;
      }
      p {
        font-size: 8;
      }
    </style>
  </head>
  <body>
''')  

LEXER = lex.lex()  #armamos el lexer
parser = yacc.yacc()
LEXER.lineno = 1
result = parser.parse(info, lexer = LEXER)
if errores == 0:
  print ("Codigo sintacticamente correcto")

html.write('</body>\n</html>')
html.close()

msvcrt.getch()

#hay que tener convencion de si usamos comillas simples o dobles, ordenar el codigo
#poner juntas las etiquetas relacionadas
#primero poner las de apertura y despues las de cierre
#eliminar lo que sobre
# hacer anotaciones breves explicando lo que ha