# LAIA CLI

**LAIA CLI** es una herramienta de línea de comandos que facilita la generación y gestión de proyectos basados en la librería [laia-gen-lib](https://pypi.org/project/laia-gen-lib/).  
Está pensada para acelerar el desarrollo de backends y APIs usando **FastAPI**, **Pydantic** y **MongoDB**.

---

## ✨ Características

- 🚀 Generación automática de modelos y CRUDs a partir de esquemas YAML.  
- ⚙️ Integración directa con **laia-gen-lib**.  
- 🛠️ Configuración sencilla de autenticación, roles y control de acceso.  
- 📦 Compatible con **PyPI** (instalación con `pip`).  
- 🔧 Comandos CLI simples y extensibles.  

---

## 📥 Instalación

Desde [PyPI](https://test.pypi.org/project/laia-cli/):

```bash
pip install laia-cli
```

Instalación en modo editable (para desarrollo):

```bash
git clone https://github.com/tuusuario/laia-cli.git
cd laia-cli
pip install -e .
```

---

## 🚀 Uso

Una vez instalada, tendrás disponible el comando laia en tu terminal.

Ejemplo básico

```bash
laia --help
```

Salida esperada:

```bash
Laia CLI

positional arguments:
  {init,start,generate-schema,help}
    init                Init new project of LAIA
    start               Start existing LAIA project
    generate-schema     Generate new OpenAPI schema
    help                Help

optional arguments:
  -h, --help            show this help message and exit
```

Inicializar un proyecto

```bash
laia init my_project
```

---

## 📄 Licencia

Este proyecto está licenciado bajo los términos de la MIT License.

---

## 🔗 Recursos

- [laia-gen-lib en PyPI](https://pypi.org/project/laia-gen-lib)

- [FastAPI Documentation](https://fastapi.tiangolo.com/)

- [Pydantic Documentation](https://docs.pydantic.dev/latest/)
