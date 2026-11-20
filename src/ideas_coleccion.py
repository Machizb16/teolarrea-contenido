"""Banco inicial de ideas de la colección LIBROS PROHIBIDOS. Añade a ideas.json las que falten.
Solo usa la información pública de docs/coleccion.md."""
import os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDEAS = os.path.join(ROOT, 'ideas.json')

HT = {
    'abras': '#NoAbrasEsteLibro #LibrosProhibidos #TeoLarrea #NovelaInteractiva #ThrillerPsicológico #Booktok #LibrosRecomendados',
    'mires': '#NoMiresEsteLibro #LibrosProhibidos #TeoLarrea #NovelaInteractiva #ThrillerPsicológico #Booktok #LibrosRecomendados',
    'creas': '#NoCreasEsteLibro #LibrosProhibidos #TeoLarrea #NovelaInteractiva #ThrillerPsicológico #Booktok #LibrosRecomendados',
}
TAGS = {
    'abras': ['no abras este libro', 'libros prohibidos', 'teo larrea', 'novela interactiva', 'booktok', 'libros recomendados'],
    'mires': ['no mires este libro', 'libros prohibidos', 'teo larrea', 'novela interactiva', 'booktok', 'libros de navidad'],
    'creas': ['no creas este libro', 'libros prohibidos', 'teo larrea', 'novela interactiva', 'booktok', 'persuasion'],
}


def P(fondo, texto=None, dur=3.7, pos=None):
    d = dict(fondo=fondo, dur=dur, texto=texto)
    if pos: d['pos'] = pos
    return d


def I(id_, libro, slug, titulo, gancho, rojo, planos, portada, descripcion):
    return dict(id=id_, libro=libro, slug=slug, titulo=titulo, gancho=gancho, rojo=rojo, planos=planos, portada=portada,
                descripcion=descripcion, hashtags=HT[libro], tags_youtube=TAGS[libro])


NOTAS = lambda *n: {'pagina': {'notas': list(n)}}
FOTO = lambda anio, cambio=None, cuenta=None: {'foto': {k: v for k, v in dict(anio=anio, cambio=cambio, cuenta=cuenta).items() if v is not None}}
MENT = lambda frases, mentira: {'mentirometro': {'frases': frases, 'mentira': mentira, 'desde': 5.0}}
PAL = ['cama', 'descanso', 'despierto', 'cansancio', 'soñar', 'almohada', 'siesta', 'manta', 'bostezo', 'pijama', 'roncar', 'noche']

A = 'abras'
ABRAS = [
    I('a01', A, 'cierrame', 'Este libro te ordena que lo cierres en la primera página',
      'ESTE LIBRO TE ORDENA QUE LO CIERRES EN LA PRIMERA PÁGINA', ['CIERRES'],
      [P('tipos'), P(NOTAS('Yo tampoco lo cerré.'), 'Si sigues leyendo, ya has desobedecido.', pos=0.3), P('faro', 'Y no eres el primero.')],
      'faro', '«Ciérrame. Ahora.» Así empieza. Si pasas la página, ya has desobedecido… y el libro lo sabe porque tú mismo se lo dices con cada decisión. ¿Lo cerrarías?'),
    I('a02', A, 'numero_0_9', 'Piensa un número del 0 al 9. Rápido.',
      'PIENSA UN NÚMERO DEL 0 AL 9. RÁPIDO.', ['RÁPIDO.'],
      [P({'numeros': {}}, dur=3.4), P({'numeros': {'resaltar': 7, 'desde': 0.6}}, '¿El 7? Es el número que más gente elige.', pos=0.3),
       P('faro', 'Este libro te hace trampas a la vista. Y luego te las explica.')],
      {'numeros': {'resaltar': 7, 'desde': 0}},
      'Cuando se pide un número del 0 al 9, el 7 es el que más se elige (Kubovy y Psotka, 1976). «No abras este libro» juega contigo con trucos así y después te los explica. ¿Cuál elegiste tú? 👇'),
    I('a03', A, 'doce_palabras', 'Memoriza estas 12 palabras (sin trampas)',
      'MEMORIZA ESTAS 12 PALABRAS', ['12'],
      [P({'palabras': PAL}, dur=6.5), P(NOTAS('¿Estaba?'), 'Sin mirar: ¿estaba la palabra DORMIR?', pos=0.3),
       P('faro', 'Mucha gente jura que sí. No estaba.')],
      {'palabras': PAL},
      'Con listas así, mucha gente «recuerda» una palabra que nunca apareció (Deese, 1959; Roediger y McDermott, 1995). En «No abras este libro» memorizas doce palabras… y el libro las guarda mejor que tú. ¿La viste? 👇'),
    I('a04', A, 'notas_margen', 'Alguien leyó este libro antes que tú. Y dejó notas.',
      'ALGUIEN LEYÓ ESTE LIBRO ANTES QUE TÚ. Y DEJÓ NOTAS.', ['NOTAS.'],
      [P(NOTAS('¿Tú también?', 'No le hagas caso.')), P('tipos', 'Notas a lápiz en los márgenes, firmadas como «M.»', pos=0.75),
       P('faro', 'Comentan tus decisiones. A veces, te contestan.')],
      NOTAS('¿Tú también?', 'No le hagas caso.'),
      'El ejemplar ya tenía un lector antes que tú: notas a lápiz con tres símbolos que discuten contigo página a página. «No abras este libro», novela interactiva de Teo Larrea.'),
    I('a05', A, 'llave_carta', 'Una llave o una carta: ¿cuál eliges?',
      'UNA LLAVE O UNA CARTA. SOLO PUEDES ELEGIR UNA.', ['UNA.'],
      [P('llave_carta', dur=4.0), P('llave_carta', 'Elige ya. Sin pensarlo.', pos=0.85),
       P('faro', 'En el libro, esa elección abre una puerta. Y cambia lo que viene después.')],
      'llave_carta',
      'En «No abras este libro» tú decides y el libro recuerda lo que decidiste. ¿Llave o carta? Responde antes de pensarlo 👇'),
    I('a06', A, 'siete_reglas', 'Para leer este libro tienes que aceptar siete reglas',
      'PARA LEER ESTE LIBRO TIENES QUE ACEPTAR SIETE REGLAS', ['SIETE'],
      [P('tipos'), P(NOTAS('Acepta.'), 'Son extrañas. Y las vas a aceptar.', pos=0.3),
       P('faro', 'No es un lector. Es parte de la historia. Tú.')],
      'tipos',
      'Siete reglas raras antes de empezar. Si las aceptas, el juego empieza contigo dentro. «No abras este libro», de Teo Larrea.'),
    I('a07', A, 'retrato_barnum', 'Voy a describirte sin conocerte',
      'VOY A DESCRIBIRTE SIN CONOCERTE', ['SIN'],
      [P(NOTAS('Te cuesta confiar.', 'Pareces seguro.', 'Por dentro, dudas.')), P('tipos', '¿Te has reconocido? A casi todo el mundo le pasa.', pos=0.75),
       P('faro', 'Se llama efecto Barnum (Forer, 1949). El libro lo usa contigo. Y luego te enseña cómo.')],
      NOTAS('Te cuesta confiar.', 'Pareces seguro.'),
      'Un retrato que parece hecho a tu medida… y vale para casi todos: es el efecto Barnum (Forer, 1949). «No abras este libro» no lee la mente: juega contigo y después vacía la manga. ¿Te has reconocido? 👇'),
    I('a08', A, 'parrafo_cambiado', 'Lee esta frase dos veces. Algo ha cambiado.',
      'LEE ESTA FRASE. LUEGO TE ENSEÑO OTRA.', ['OTRA.'],
      [P(NOTAS('Abrió la puerta despacio', 'y entró en la cocina.'), dur=4.2),
       P(NOTAS('Abrió la puerta despacio', 'y entró en la casa.'), '¿Qué palabra ha cambiado?', dur=4.2, pos=0.3),
       P('faro', 'Mucha gente no lo nota (Sturt, Sanford y otros, 2004).')],
      NOTAS('Abrió la puerta despacio', 'y entró en la cocina.'),
      'Leemos por encima y no notamos cambios pequeños en un texto (Sturt, Sanford y otros, 2004). En «No abras este libro» lees el mismo párrafo dos veces… ¿lo notaste a la primera? 👇'),
    I('a09', A, 'apuesta', 'Este libro te reta a una apuesta',
      'ESTE LIBRO TE RETA A UNA APUESTA', ['APUESTA'],
      [P('llave_carta'), P(NOTAS('No apuestes.'), '«Un tahúr no miente. Elige qué carta enseña.»', pos=0.3),
       P('faro', 'Apuesta contra el libro. A ver quién gana.')],
      'llave_carta',
      'El narrador es el propio libro, con voz de tahúr educado. Te propone una apuesta… y tú decides si aceptas. «No abras este libro», de Teo Larrea.'),
    I('a10', A, 'memoria', 'A ti se te olvidarán cosas. A este libro, ninguna.',
      'A TI SE TE OLVIDARÁN COSAS. A ÉL, NINGUNA.', ['NINGUNA.'],
      [P('faro'), P(NOTAS('Lo apunta todo.'), 'Recuerda cada decisión que tomas dentro del libro.', pos=0.3),
       P('tipos', 'Y te la devuelve cuando menos lo esperas.', pos=0.75)],
      'faro',
      '«Lo que sí tengo es memoria. Y buena letra.» El libro no te ve ni te oye, pero recuerda lo que elegiste. «No abras este libro», novela interactiva.'),
    I('a11', A, 've_al_fragmento', 'Un libro que no se lee de principio a fin',
      'ESTE LIBRO NO SE LEE DE PRINCIPIO A FIN', ['FIN'],
      [P(NOTAS('Ve al 12.')), P('tipos', 'Fragmentos numerados. Tú eliges adónde saltas.', pos=0.75),
       P('faro', 'En papel o en Kindle. Sin escribir en el libro.')],
      NOTAS('Ve al 12.'),
      'Novela interactiva en segunda persona: lees, decides y saltas al fragmento que te toca. Funciona igual en tapa blanda y en Kindle. «No abras este libro».'),
    I('a12', A, 'tres_destellos', 'Tres destellos y una pausa',
      'TRES DESTELLOS Y UNA PAUSA', ['PAUSA'],
      [P('faro', dur=5.0), P('faro', 'Un faro, una casa de veraneo y una imprenta antigua.'),
       P(NOTAS('Empieza como un juego.'), 'Empieza como un juego. Acaba tocándote dentro.', pos=0.3)],
      'faro',
      'El faro de Cabo Silvo marca el ritmo de «No abras este libro»: tres destellos y una pausa. Un juego inquietante que se convierte en una historia muy humana.'),
    I('a13', A, 'adivina', 'Pídele a este libro que adivine',
      'PÍDELE A ESTE LIBRO QUE ADIVINE', ['ADIVINE'],
      [P({'numeros': {}}), P('llave_carta', 'No lee la mente. Juega contigo.', pos=0.85),
       P('faro', 'Hace trampas a la vista. Y luego vacía la manga.')],
      {'numeros': {}},
      'El libro no adivina de verdad: hace trucos delante de ti y luego te explica cada uno. ¿Le pedirías que adivinara? «No abras este libro», de Teo Larrea.'),
    I('a14', A, 'recuerdo_contagiado', 'Un recuerdo puede no ser del todo tuyo',
      'TU RECUERDO PUEDE NO SER DEL TODO TUYO', ['TUYO'],
      [P(NOTAS('Había una tostadora.', 'Seguro que sí.')),
       P('tipos', 'Si alguien recuerda algo contigo, puedes acabar recordándolo tú.', pos=0.75),
       P('faro', 'Contagio social de la memoria (Roediger, Meade y Bergman, 2001).')],
      NOTAS('Había una tostadora.'),
      'Los recuerdos se «contagian»: lo que otro dice que vio puede colarse en tu memoria (Roediger, Meade y Bergman, 2001). «No abras este libro» juega con tu memoria y te lo explica.'),
    I('a15', A, 'regalo_desobedientes', 'El libro perfecto para quien nunca hace caso',
      'EL LIBRO PERFECTO PARA QUIEN NUNCA HACE CASO', ['NUNCA'],
      [P('faro'), P(NOTAS('Ábrelo.'), 'Novela interactiva. En papel o en Kindle.', pos=0.3),
       P('llave_carta', 'Regálaselo a quien siempre abre lo que no debe.', pos=0.85)],
      'faro',
      '«Libros que te prohíben algo. Y que, en cuanto desobedeces, ya no te sueltan.» ¿A quién se lo regalarías? Etiquétalo 👇'),
]

M = 'mires'
CAMBIOS = [('m02', 1994, 'estrella', 'Falta la estrella del árbol.'), ('m03', 1995, 'lampara', 'La lámpara está apagada.'),
           ('m04', 1993, 'cuadro', 'El cuadro de la pared está torcido.'), ('m05', 1997, 'vela', 'Falta una de las velas.'),
           ('m06', 1999, 'cortina', 'La cortina de la izquierda está corrida.')]
GANCHOS_C = ['¿QUÉ HA CAMBIADO ENTRE ESTAS DOS FOTOS?', 'DOS FOTOS. UN CAMBIO. ¿LO VES?', 'ENCUENTRA LA DIFERENCIA EN DIEZ SEGUNDOS',
             'SOLO UNA COSA ES DISTINTA. ¿CUÁL?', 'MISMO SALÓN. MISMA FAMILIA. UNA DIFERENCIA.']
MIRES = [
    I('m01', M, 'mira_10_segundos', 'Mira esta foto 10 segundos. Luego te pregunto.',
      'MIRA ESTA FOTO 10 SEGUNDOS. LUEGO TE PREGUNTO.', ['10'],
      [P(FOTO(1991, cuenta=10), dur=10.0), P('camara', '¿Cuántas velas había en la mesa?', pos=0.25),
       P(FOTO(1991), 'Eran tres. ¿Acertaste?', pos=0.86)],
      FOTO(1991),
      '«Mírala diez segundos. Luego pasa la página. Y no vuelvas.» Así se juega «No mires este libro»: mirar, recordar y responder sin volver atrás. ¿Acertaste? 👇'),
]
TITULOS_C = ['¿Qué ha cambiado entre estas dos fotos?', 'Dos fotos, un cambio: ¿lo ves?', 'Encuentra la diferencia en diez segundos',
             'Solo una cosa es distinta: ¿cuál?', 'Mismo salón, misma familia, una diferencia']
for (id_, anio, cambio, sol), g, tt in zip(CAMBIOS, GANCHOS_C, TITULOS_C):
    MIRES.append(I(id_, M, f'cambio_{cambio}', tt, g, ['CAMBIO.', 'DIFERENCIA', 'DISTINTA.', 'CAMBIADO'],
                   [P(FOTO(anio), dur=4.0), P(FOTO(anio, cambio), 'Mírala bien.', dur=4.5, pos=0.86),
                    P(FOTO(anio, cambio), sol + ' ¿Lo viste?', pos=0.86)],
                   FOTO(anio),
                   'Cuesta mucho ver un cambio entre dos imágenes casi iguales: se llama ceguera al cambio (Simons y Rensink, 2005). '
                   '«No mires este libro» son doce fotos de Nochebuena casi idénticas… ¿lo viste a la primera? 👇'))
MIRES += [
    I('m07', M, 'doce_nochebuenas', 'La misma foto, doce Nochebuenas seguidas',
      'LA MISMA FOTO. DOCE NOCHEBUENAS SEGUIDAS.', ['DOCE'],
      [P(FOTO(1990)), P(FOTO(1995), 'Mismo salón. Mismo encuadre. Las nueve de la noche.', pos=0.86),
       P('camara', 'Diez segundos de disparador. Y él corriendo a su sitio.', pos=0.25)],
      FOTO(1990),
      'De 1990 a 2001, Tomás Arranz, relojero, hizo cada Nochebuena la misma foto de su familia. Doce fotos casi idénticas. «No mires este libro», de Teo Larrea.'),
    I('m08', M, 'nochebuena_1996', 'De la Nochebuena de 1996 nadie habla',
      'DE LA NOCHEBUENA DE 1996 NADIE HABLA', ['1996'],
      [P('camara'), P('telefono', 'Una nevada. Un apagón. «Papá estaba raro».'),
       P('camara', '«Yo no recuerdo. Yo fijo.»', pos=0.25)],
      'camara',
      'Cada uno la recuerda a su manera. La cámara, en cambio, no recuerda: fija. «No mires este libro», thriller psicológico interactivo con un final luminoso.'),
    I('m09', M, 'narra_una_camara', 'Este libro lo cuenta una cámara de fotos',
      'ESTE LIBRO LO CUENTA UNA CÁMARA DE FOTOS', ['CÁMARA'],
      [P('camara'), P(FOTO(1992), 'Paciente, precisa y con humor seco.', pos=0.86),
       P('camara', '«Ponte detrás de mí.»', pos=0.25)],
      'camara',
      'El narrador de «No mires este libro» es la cámara que hizo las fotos. Te pide que te pongas detrás de ella y mires donde nadie mira.'),
    I('m10', M, 'no_lo_viste', 'Mientras miras una cosa, te pierdes otra',
      'MIENTRAS MIRAS UNA COSA, TE PIERDES OTRA', ['OTRA'],
      [P('cuenta_atras', dur=4.0), P(FOTO(1993), 'Si te concentras en algo, puedes no ver lo que tienes delante.', pos=0.86),
       P('camara', 'Ceguera por falta de atención (Simons y Chabris, 1999).', pos=0.25)],
      'cuenta_atras',
      'Es el famoso experimento del gorila invisible (Simons y Chabris, 1999). «No mires este libro» se juega con esa idea: las respuestas están en las fotos desde el principio.'),
    I('m11', M, 'foto_y_recuerdo', 'Una foto puede cambiar lo que recuerdas',
      'UNA FOTO PUEDE CAMBIAR LO QUE RECUERDAS', ['RECUERDAS'],
      [P(FOTO(1990)), P('telefono', 'Una foto retocada puede hacerte recordar algo que nunca pasó.'),
       P('camara', 'Lo estudiaron Wade, Garry, Read y Lindsay (2002).', pos=0.25)],
      FOTO(1990),
      '¿Tu Nochebuena fue como la recuerdas… o como sale en la foto? (Wade, Garry, Read y Lindsay, 2002). «No mires este libro», de Teo Larrea.'),
    I('m12', M, 'mira_donde_nadie', 'Las respuestas están en las fotos desde el principio',
      'LAS RESPUESTAS ESTÁN EN LAS FOTOS DESDE EL PRINCIPIO', ['PRINCIPIO'],
      [P(FOTO(1997)), P('camara', 'Solo hay que mirar donde nadie mira.', pos=0.25),
       P('cuenta_atras', 'Mírala diez segundos. Y no vuelvas atrás.', dur=4.0, pos=0.22)],
      FOTO(1997),
      '«Mira donde nadie mira.» Una novela interactiva que se juega mirando: 119 fragmentos y doce fotos de familia. «No mires este libro».'),
    I('m13', M, 'regalo_navidad', 'Un regalo de Navidad que se lee mirando',
      'UN REGALO DE NAVIDAD QUE SE LEE MIRANDO', ['NAVIDAD'],
      [P(FOTO(1998)), P('camara', 'Secretos de familia guardados a la vista de todos.', pos=0.25),
       P('telefono', 'Y un final luminoso. Para leer en Navidad.')],
      FOTO(1998),
      'Una cena de Nochebuena, una familia y doce fotos casi iguales. «No mires este libro» es el regalo perfecto para estas fiestas 🎄'),
    I('m14', M, 'la_familia', 'Siete personas, una cena, doce años',
      'SIETE PERSONAS. UNA CENA. DOCE AÑOS.', ['DOCE'],
      [P(FOTO(1992)), P(FOTO(1992), 'Tomás, el relojero. Pilar. Marta, que lo organiza todo.', pos=0.86),
       P(FOTO(1998), 'Javier y su cigarro apagado. Luis, el bromista. Sara y Dani.', pos=0.86)],
      FOTO(1992),
      'La familia Arranz posa cada Nochebuena en el mismo salón de Valdecierva. Tú miras, recuerdas y respondes. «No mires este libro».'),
    I('m15', M, 'anos_noventa', 'Teléfono de disco, apagones y Nochebuena en familia',
      'TELÉFONO DE DISCO, APAGONES Y NOCHEBUENA EN FAMILIA', ['NOCHEBUENA'],
      [P('telefono'), P(FOTO(1991), 'Valdecierva, calle Alfareros. Años noventa.', pos=0.86),
       P('camara', 'Una novela que se juega mirando.', pos=0.25)],
      'telefono',
      'La España de los noventa, una familia y una cámara en trípode. «No mires este libro», novela interactiva de Teo Larrea.'),
]

C = 'creas'
MENTIRAS = [
    ('c02', ['El pulpo tiene tres corazones.', 'La Gran Muralla se ve desde la Luna a simple vista.', 'La miel bien guardada puede durar siglos.'], 1,
     'La Gran Muralla no se ve a simple vista desde la Luna: es un mito muy repetido.'),
    ('c03', ['Los murciélagos son ciegos.', 'Venus gira al revés que casi todos los planetas.', 'Escocia tiene el unicornio como animal nacional.'], 0,
     'Los murciélagos no son ciegos: ven, y muchos además usan la ecolocalización.'),
    ('c04', ['Los tiburones son más antiguos que los árboles.', 'Un rayo puede caer dos veces en el mismo sitio.', 'Solo usamos el 10 % del cerebro.'], 2,
     'Lo del 10 % del cerebro es un mito: usamos todo el cerebro, aunque no todo a la vez.'),
    ('c05', ['Los camellos guardan agua en la joroba.', 'Los flamencos son rosas por lo que comen.', 'Los plátanos son bayas y las fresas no.'], 0,
     'La joroba del camello guarda grasa, no agua.'),
]
CREAS = [
    I('c01', C, 'siete_mentiras', 'Un libro que te avisa: te voy a mentir siete veces',
      'UN LIBRO QUE TE AVISA: TE VOY A MENTIR SIETE VECES', ['SIETE'],
      [P('sobre'), P({'rayas': 7}, 'Encuéntralas.', pos=0.35),
       P('pueblo', 'Lo difícil es saber cuál te has creído.')],
      'sobre',
      '«En este libro te voy a mentir siete veces. Encuéntralas.» Julián Ferrer, timador retirado, te cuenta su mejor golpe. ¿Cuántas encontrarías? 👇'),
]
for id_, fr, k, sol in MENTIRAS:
    CREAS.append(I(id_, C, f'mentirometro_{id_}', 'Mentirómetro: una de estas tres frases es mentira',
                   'UNA DE ESTAS TRES FRASES ES MENTIRA', ['MENTIRA'],
                   [P('pueblo', dur=2.6), P(MENT(fr, k), dur=7.5), P({'rayas': 1}, '¿Acertaste? En el libro hay seis Mentirómetros.', pos=0.35)],
                   'sobre',
                   f'{sol} En «No creas este libro», un timador te miente siete veces y seis veces el libro se para en un Mentirómetro. ¿Cuál elegiste? 👇'))
CREAS += [
    I('c06', C, 'favor_deuda', 'Si te hacen un favor, te sientes en deuda. Los timadores lo saben.',
      'SI TE HACEN UN FAVOR, TE SIENTES EN DEUDA', ['DEUDA'],
      [P('pueblo'), P('sobre', 'Se llama reciprocidad. Es una de las técnicas de persuasión de Cialdini.', pos=0.8),
       P({'rayas': 2}, 'Julián la usa en un pueblo entero. Y contigo.', pos=0.35)],
      'pueblo',
      'El favor que obliga: una de las técnicas de persuasión que describió Cialdini. En «No creas este libro», Julián te enseña cada truco mientras lo usa contigo.'),
    I('c07', C, 'verdad_ilusoria', 'Si lo oyes muchas veces, acabas creyéndolo',
      'SI LO OYES MUCHAS VECES, ACABAS CREYÉNDOLO', ['CREYÉNDOLO'],
      [P('pueblo'), P({'telegrama': ['EL AGUA CURA STOP', 'EL AGUA CURA STOP', 'EL AGUA CURA STOP']}, dur=4.0),
       P('anuncio', 'Efecto de verdad ilusoria (Hasher, Goldstein y Toppino, 1977).', pos=0.86),
       P('sobre', 'Pasa incluso cuando sabes que es falso (Fazio y otros, 2015).', pos=0.8)],
      'pueblo',
      'Repetir una frase la hace parecer más verdadera, aunque sepamos que es falsa. Julián lo sabía en 1978. «No creas este libro», de Teo Larrea.'),
    I('c08', C, 'anclaje_precio', '¿Cuánto pagarías por esta botella de agua?',
      '¿CUÁNTO PAGARÍAS POR UNA BOTELLA DE AGUA?', ['AGUA?'],
      [P('pueblo'), P('anuncio', 'Primero te dicen un precio altísimo. Luego, otro «barato».', pos=0.86),
       P('sobre', 'Ese primer número te ancla (Tversky y Kahneman, 1974).', pos=0.8)],
      'pueblo',
      'El anclaje del precio: el primer número que oyes condiciona todo lo demás. En Fuensanta del Río alguien vendía agua milagrosa… «No creas este libro».'),
    I('c09', C, 'pie_en_la_puerta', 'Primero un sí pequeñito. Luego, el grande.',
      'PRIMERO UN SÍ PEQUEÑITO. LUEGO, EL GRANDE.', ['GRANDE.'],
      [P('pueblo'), P({'rayas': 1}, 'Un compromiso pequeño hace más fácil el siguiente.', pos=0.35),
       P('sobre', 'Se llama «pie en la puerta» (Freedman y Fraser, 1966).', pos=0.8)],
      'pueblo',
      'Así se empieza: con algo tan pequeño que no puedes decir que no. «No creas este libro» te enseña los trucos de un timador desde dentro.'),
    I('c10', C, 'detectar_mentiras', 'Crees que sabes cuándo te mienten',
      'CREES QUE SABES CUÁNDO TE MIENTEN', ['MIENTEN'],
      [P('sobre'), P({'rayas': 3}, 'Detectamos mentiras casi al azar (Bond y DePaulo, 2006).', pos=0.35),
       P('pueblo', 'Julián cuenta con ello. Y te lo dice a la cara.')],
      'sobre',
      'La ciencia dice que pillamos mentiras casi al azar (Bond y DePaulo, 2006). ¿Serás capaz de encontrar las siete de este libro? 👇'),
    I('c11', C, 'bata_y_sello', 'Una bata y un sello. No hace falta más.',
      'UNA BATA Y UN SELLO. NO HACE FALTA MÁS.', ['SELLO.'],
      [P('sobre'), P('anuncio', 'Un análisis de laboratorio. Un sello oficial.', pos=0.86),
       P('pueblo', 'La autoridad convence antes de que pienses.')],
      'sobre',
      'La autoridad es otra de las técnicas de persuasión de Cialdini. En «No creas este libro» la ves funcionar en un pueblo de la sierra en 1978.'),
    I('c12', C, 'plazas_limitadas', 'Plazas limitadas. Solo hoy.',
      'PLAZAS LIMITADAS. SOLO HOY.', ['HOY.'],
      [P('sobre'), P('anuncio', 'La prisa y la escasez apagan las preguntas.', pos=0.86),
       P('pueblo', '«En Fuensanta se lo creyeron todos.»')],
      'sobre',
      'Cuando algo se acaba, dejamos de pensar. Julián Ferrer lo usó en Fuensanta del Río. ¿Tú habrías picado? 👇 «No creas este libro».'),
    I('c13', C, 'mejor_golpe', 'Un timador de 79 años te cuenta su mejor golpe',
      'UN TIMADOR DE 79 AÑOS TE CUENTA SU MEJOR GOLPE', ['GOLPE'],
      [P('pueblo'), P({'telegrama': ['VERANO 1978 STOP', 'LLEGA FORASTERO STOP', 'TRAJE GRIS STOP']}, dur=4.0),
       P('sobre', '«Me dedicaba a convencer a la gente.»', pos=0.8)],
      'pueblo',
      'Verano de 1978. Un forastero de traje gris llega a un pueblo de cuatrocientos vecinos con un maletín y una idea. «No creas este libro», de Teo Larrea.'),
    I('c14', C, 'ines', 'Una niña de 12 años era la única que no se creía nada',
      'UNA NIÑA DE 12 AÑOS ERA LA ÚNICA QUE NO SE CREÍA NADA', ['NADA'],
      [P('pueblo'), P('anuncio', 'Cuatrocientos vecinos. Un agua milagrosa. Y una niña con preguntas.', pos=0.86),
       P('sobre', '¿Tú habrías sido Inés?', pos=0.8)],
      'pueblo',
      'En Fuensanta del Río casi todos se dejan convencer. Inés, de 12 años, no se cree nada. ¿Y tú? «No creas este libro».'),
    I('c15', C, 'protegerte_timo', 'Cómo darte cuenta de un timo, explicado por un timador',
      'CÓMO DARTE CUENTA DE UN TIMO (LO EXPLICA UN TIMADOR)', ['TIMO'],
      [P('pueblo'), P({'telegrama': ['PRISA STOP', 'FAVORES STOP', 'PRECIO ANCLA STOP']}, dur=4.0),
       P({'rayas': 7}, 'El libro acaba con un apéndice real: cómo protegerte de un timo.', pos=0.35)],
      'pueblo',
      'Simpatía, autoridad, favores, prisa… Julián te enseña los trucos y el libro termina con consejos reales para que no te la cuelen. «No creas este libro».'),
]


def main():
    ideas = json.load(open(IDEAS)); ya = {i['id'] for i in ideas}
    nuevas = [i for i in ABRAS + MIRES + CREAS if i['id'] not in ya]
    for i in nuevas: assert len(i['titulo']) <= 90, i['id']
    ideas += nuevas
    json.dump(ideas, open(IDEAS, 'w'), ensure_ascii=False, indent=1)
    print('añadidas', len(nuevas), 'total', len(ideas))


if __name__ == '__main__':
    main()
