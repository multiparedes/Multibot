# **Multibot, un bot de discord escrito en python. 🐍**

Multibot es un bot simple de Discord con algunas funcionalidades. Empecé este proyecto para ver hasta donde podía hacer con un conocimiento simple de Python.

⚠️ **ATENCIÓN**  : Esta no es una versión definitiva, me gustaría seguir aumentando las funcionalidades a medida que aprendo más.

---

###  **1. Añadir Multibot a un servidor 🤖** 

Para añadir este bot a tu servidor de Discord es muy sencillo, solo tienes que pulsar en el siguiente link y seleccionar el servidor que quieras. 

    https://discord.com/api/oauth2/authorize?client_id=859364355979608064&permissions=8&scope=bot

📝 : *Para poder añadir este bot debes ser admin del servidor en cuestión.*    

<br>

### **2. Instalar Multibot en tu ordenador ⚙️** 

Al este ser un proyecto de código libre cualquiera puede modificar el código fuente y hacer su propia versión del bot. Actualmente el bot no está hosteado en ningún lado por lo tanto es una opción para ver el funcionamiento del bot alojandolo en tu própio ordenador.

**Requisitos:**

- Python3 o superior.
- La libreria ``discord.py``, la puedes obtener con el comando ``pip install discord.py`` en la consola.
- Un archivo en la misma carpeta llamado ``secret.env`` con el token privado del bot. *Solo el token, sin comillas ni nada extra.*

Una vez todo está instalado y los requisitos cumplidos simplemente ejecuta el archivo llamado ``main.py``, no hacen falta permisos de administrador.

<br>

### **3. Lista de comandos disponibles. 📔**

*Comandos varios:*\
ayuda : Muestra este mensaje.\
​ping : Devuelve la latencia actual del bot.\
​borrar : Borra el numero especificado de mensajes del canal actual.\
​nuke : Borra todos los mensajes del canal actual.\
​nick : Comando para poner un nick a algun usuario.\
​unnick : Comando para poner quitar el nick a algun usuario.\
​precio : Devuelve el precio de la criptomoneda en euros y dolares.

*Comandos de administrador (necesario rol Admin):*\
kick : Expulsa a un usuario del servidor.\
​ban : Banea a un usuario del servidor.\
​unban : Desbanea a un usuario del servidor.

Mas comandos y funcionalidades estan por venir.

---

<br>

Esta es una version muy experimental del bot. Para cualquier bug, problema o sugerimiento no dudes en enviarme un DM por Discord:  ``Multiparedes#1982`` ❤️