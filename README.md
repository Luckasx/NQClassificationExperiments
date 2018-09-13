## NQClassificationExperiments
This repository contains the files needed to reproduce the experiments of the article *WANQA: uma Abordagem para Identificar Novas Questões Não Respondíveis em Comunidades de Perguntas e Respostas* published in the SBBD 2018.

### Pre Requisite
Rapidminer Studio 7.6+

### Pre Requisite B1 Experiments

Install the extension SSFS_APSO (https://github.com/Luckasx/RMExtension_SSFSAPSO) with Gradle.

### Required Rapidminer Plugins

 * Text Processing
 * Web Mining
 * Weka

### Steps to reproduce the main experiments

1.  Download and Extract the content of the zip *backup_rapidminer_20180226.zip*

2.  Close the Rapidminer Studio and copy all the content of the folder **Local Repository** to the **C:\Users\\%USERNAME%\\.RapidMiner\repositories\Local Repository\** (Windows) or the equivalent folder.

3.  The 3 Questions datasets are under the **data** folder and the processes under the **processes** folder.

4.  To run the experiments just fill the required parameters and play.

* The original dataset obtained from StackExchange is at the *cqadb_20171211.zip* as a SqliteDB.
 

