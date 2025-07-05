FROM  3.14-rc-slim-bookworm
COPY target/java-web-app.war  /usr/local/tomcat/webapps/java-web-app.war
