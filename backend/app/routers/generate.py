import os
from fastapi import APIRouter
from pydantic import BaseModel, validator

import torch
from transformers import GPT2TokenizerFast, GPT2LMHeadModel

tokenizer_path = '/backend/app/artifacts/gpt2_tokenizer_fast'
model_path = '/backend/app/artifacts/gpt2_default'

if not os.path.exists(tokenizer_path):
    tokenizer = GPT2TokenizerFast.from_pretrained('gpt2')
    tokenizer.save_pretrained(tokenizer_path)
else:
    tokenizer = GPT2TokenizerFast.from_pretrained(tokenizer_path)

if not os.path.exists(model_path):
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    model.save_pretrained(model_path)
else:
    model = GPT2LMHeadModel.from_pretrained(model_path)

TEMPRATURE = 0.7
PENALTY_ALPHA = 0.75
TOP_K = 50
TOP_P = 0.95
DO_SAMPLE = True
PAD_TOKEN_ID = tokenizer.eos_token_id

class Prompt(BaseModel):
    text: str = " "
    response_length: int = 25

    @validator('text')
    def text_less_than_512(cls, text):
        tokenized_text = tokenizer(text, return_tensors="pt")
        if len(tokenized_text['input_ids']) >= 512:
            raise ValueError('Context must be less than 512 tokens.')
        return text

    @validator('response_length')
    def response_length_less_than_200(cls, value):
        if value > 200:
            raise ValueError('Reponse length must be less than 200 tokens')
        return value

router = APIRouter(prefix='/generate')

@router.post('/')
def generate(prompt: Prompt):
    encoded_input = tokenizer(prompt.text, return_tensors="pt")

    output_sequences_conservative = model.generate(
        input_ids=encoded_input['input_ids'],
        max_length=prompt.response_length,
        temperature=TEMPRATURE,
        penalty_alpha=PENALTY_ALPHA,
        top_k=TOP_K,
        top_p =TOP_P,
        do_sample=DO_SAMPLE,
        pad_token_id=PAD_TOKEN_ID,
        )

    output_sequences_liberal = model.generate(
        input_ids=encoded_input['input_ids'],
        max_length=prompt.response_length,
        temperature=TEMPRATURE,
        penalty_alpha=PENALTY_ALPHA,
        top_k=TOP_K,
        top_p =TOP_P,
        do_sample=DO_SAMPLE,
        pad_token_id=PAD_TOKEN_ID,
        )
    
    generated_text_conservative = tokenizer.decode(output_sequences_conservative[0], skip_special_tokens=True)
    generated_text_liberal = tokenizer.decode(output_sequences_liberal[0], skip_special_tokens=True)

    conservative_response = generated_text_conservative[len(tokenizer.decode(encoded_input['input_ids'][0], skip_special_tokens=True)):].strip()
    liberal_response = generated_text_liberal[len(tokenizer.decode(encoded_input['input_ids'][0], skip_special_tokens=True)):].strip()

    return {
        'prompt': prompt.text,
        'conservative': conservative_response,
        'liberal': liberal_response
    }

@router.get('/test_device')
def test_device():
    if torch.cuda.is_available():
        device = 'cuda'
    else:
        device = 'cpu'

    return {"device": device}

