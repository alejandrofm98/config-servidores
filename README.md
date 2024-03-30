# config-servidores
Configuracion de los servidores utilizados para el proyecto restaurantrq.

## Servicios

#### Jenkins
Permite implementar CI/CD en los diferentes proyectos. <br/>
Se utilizan pipelines para el despliegue de los proyectos, podemos encontrar <br/>
jenkinsfile en este repositorio <br/>
Jenkins esta instalado en el servidor de producción y podemos acceder con la siguiente url: <br/>
http://restaurantejww.ddns.net:8081/login?from=%2F

#### FileBrowser
Se utiliza para ver/modificar los ficheros donde se despliega el proyecto <br/>
Principalmente utilizado para ver los logs del backend <br/>
Esta montando el servidor de desarrollo. <br/>
http://restaurantejww-des.ddns.net:8200/login?redirect=%2Ffiles%2F

#### Aplicacion
En este caso tenemos el docker compose para levantar la aplicacion java (SrpringBoot) <br/>
y la base de datos a la misma vez.

#### Servidor
Script inicial para realizar la configuración basica del servidor.
