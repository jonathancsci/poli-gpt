import os
from fastapi import APIRouter
from pydantic import BaseModel, validator

import torch
from transformers import GPT2TokenizerFast, GPT2LMHeadModel

tokenizer_path = '/backend/app/artifacts/gpt2_tokenizer_fast'
conservative_model_path = '/backend/app/artifacts/conservative-gpt2'
liberal_model_path = '/backend/app/artifacts/liberal-gpt2'

if not os.path.exists(tokenizer_path):
    tokenizer = GPT2TokenizerFast.from_pretrained('gpt2')
    tokenizer.save_pretrained(tokenizer_path)
else:
    tokenizer = GPT2TokenizerFast.from_pretrained(tokenizer_path)

if not os.path.exists(conservative_model_path):
    conservative_model = GPT2LMHeadModel.from_pretrained('jonathancsci/conservative-gpt2')
    conservative_model.save_pretrained(conservative_model_path)
else:
    conservative_model = GPT2LMHeadModel.from_pretrained(conservative_model_path)

if not os.path.exists(liberal_model_path):
    liberal_model = GPT2LMHeadModel.from_pretrained('jonathancsci/liberal-gpt2')
    liberal_model.save_pretrained(liberal_model_path)
else:
    liberal_model = GPT2LMHeadModel.from_pretrained(liberal_model_path)

conservative_model = conservative_model.to('cuda')
conservative_model.eval()
liberal_model = liberal_model.to('cuda')
liberal_model.eval()

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
    def response_length_less_than_512(cls, value):
        if value >= 512:
            raise ValueError('Reponse length must be less than 512 tokens')
        return value

router = APIRouter(prefix='/generate')

@router.post('/')
def generate(prompt: Prompt):
    encoded_input = tokenizer(prompt.text, return_tensors="pt").to('cuda')

    with torch.no_grad():
        output_sequences_conservative = conservative_model.generate(
            input_ids=encoded_input['input_ids'],
            max_length=prompt.response_length,
            temperature=0.7,
            top_k=55,
            top_p=0.95,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.015,
            no_repeat_ngram_size=6,
            )

        output_sequences_liberal = liberal_model.generate(
            input_ids=encoded_input['input_ids'],
            max_length=prompt.response_length,
            temperature=0.7,
            top_k=50,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.01,
            no_repeat_ngram_size=6,
            )
    
    # Response with the prompt
    generated_text_conservative = tokenizer.decode(output_sequences_conservative[0], skip_special_tokens=True)
    generated_text_liberal = tokenizer.decode(output_sequences_liberal[0], skip_special_tokens=True)

    # Strip the prompt from each response
    prompt_length = len(tokenizer.decode(encoded_input['input_ids'][0], skip_special_tokens=True))
    conservative_response = generated_text_conservative[prompt_length:].strip()
    liberal_response = generated_text_liberal[prompt_length:].strip()

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

