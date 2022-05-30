# SOURCE LINK GENERATOR

The program allows you to generate a list of references from references to articles for further use in term papers or dissertations.

The application has an interactive mode, a mode of reading from command line arguments, reading from a file. Optionally, you can set the amount by which the dates of calls will be randomly shifted so that the list looks more realistic.

## Usage

1. Clone repo
    
    ```bash
    git clone https://github.com/FunckingCat/source-link-generator.git
    cd source-link-generator
    ```
    
2. Create venv and Install dependencies
    
    ```bash
    python3 -m venv env 
    source ./env/bin/activate
    pip install -r rec
    ```
    
3. Application has many tips to help you use it
    
    ```bash
    usage: main.py [-h] (-i | -u URL | -f FILE) [-s SPAN]
    
    optional arguments:
      -h, --help            show this help message and exit
      -i, --inter           turns on interactive mode
      -u URL, --url URL     site url to parse
      -f FILE, --file FILE  source file with links, one per line
      -s SPAN, --span SPAN  time-span to flash-back date of the application
    ```
    
4. Generate links!!!
    
    ```bash
    (env) user@mac slg % python main.py -u https://all-python.ru/osnovy/tsvetnoj-vyvod-teksta.html -s 4
    Result: 
    Цветной вывод текста в Python [Электронный ресурс]. – URL: https://all-python.ru/osnovy/tsvetnoj-vyvod-teksta.html (дата обращения: 28.05.2022).
    ```