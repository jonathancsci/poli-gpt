# PoliGPT
__Project for ATLS 4214: Big Data Architecture__

PoliGPT is a web application that allows users to compare the differences between liberal and conservative news. Users can generate from both liberal and conservative GPT-2 models with the same prompt and visualize both responses side by side. Users can also use a basic text search to browse news articles that were used to train the models.
## Models and Dataset
More information regarding the models and dataset are available on Hugging Face:
- [liberal-gpt2](https://huggingface.co/jonathancsci/liberal-gpt2)
- [conservative-gpt2](https://huggingface.co/jonathancsci/conservative-gpt2)
- [liberal-and-conservative-news dataset](https://huggingface.co/datasets/jonathancsci/liberal-and-conservative-news)
## Running the project
1. Clone the repository (for systems without CUDA, use the 'cpu' branch)
2. Download the two .csv files from [liberal-and-conservative-news dataset](https://huggingface.co/datasets/jonathancsci/liberal-and-conservative-news) and place them in the `backend/app/data/` directory
3. In the root of the project, run `docker compose up` (this may take from 10min-1hr to complete, depending on your system)
## Setting up for development
1. Make sure you are in the root of the project
2. Create a .env file with the following fields:
```.env
POSTGRES_PASSWORD=your_value
POSTGRES_USER=your_value
POSTGRES_DB=your_value
```
3. Use python 3.10+ to create a venv and install dependencies
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## License
This software is licensed under the [`MIT-0`](https://github.com/aws/mit-0) license. The intent is to effectively place this work in the public domain.