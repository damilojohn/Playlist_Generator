#importing libraries
import gradio as gr 
import transformers 
from sentence_transformers import SentenceTransformer,util
import pickle 
import pandas as pd 


songs_df = 
verses_df = 
song_embeddings = pickle.load()

embedder = SentenceTransformer('')


def generate_playlist(prompt):
  prompt_embed = embedder.encode(prompt)
  hits = util.semantic_search(prompt_embed,song_embeddings,top_k=20)
  hits = pd.DataFrame.from_dict(hits[0])
  verses_match = verses_df.iloc[hits['corpus_id']]
  verses_match = verses_match.drop_duplicates(subset='song_id')
  songs_match = songs_df[songs_df['song_id'].isin(verses_match['song_id'].values)
  songs_match.song_id = pd.Categorical(songs_match.song_id,categories=verses_match['song_id'].values)
  songs_match = songs_match.sort_values('song_id')
  songs_match = songs_match.loc[0:9] 
  songs_name = list(songs_match['full-title'])
  return gr.Radio.update(label='songs',interactive=True,choices=song_name)


def set_example_prompt(examples):
  return gr.TextArea.update(value=examples[0]) 
  
  
  
demo = gr.Blocks()
with demo:
  gr.Markdown(
      ''' 
      # A playlist Generator for Afrobeats
      '''
  )
  with gr.Row():
    with gr.Column():
      gr.Markdown(
          '''
          Enter a Prompt to generate a playlist based on that prompt 
          '''
      )
      song_prompt = gr.TextArea(
          value='I need igbo and shayo',
          placeholder = "Enter a sentence that describes how you're feeling or what you want your playlist to be about"
      )
      example_prompts = gr.Dataset(
          components=[song_prompt]
          samples= [
              ['Lazy day'],
              ['I need money'],
              ['nobody gets me ']
          ]
      )
    with gr.Column():
      fetch_songs = gr.Button(value='generate your playlist',).style(full_width=True)
      with gr.Row():
        song_options = gr.Radio(label='songs',interactive=True,choices=None,type='value')
    with gr.Column():
      lyrics = gr.Textbox((label='lyrics',placeholder="select a song to see it's lyrics"))
    fetch_songs.click(
        fn=generate_playlist,
        inputs=[song_prompt],
        outputs=[song_option]
    )
    example_prompts.click(
        fn=set_example_prompts,
        inputs = [example_prompts],
        output = example_prompts.components
    )
  

  demo.launch(debug=True)