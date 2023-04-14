#importing libraries
import transformers 
import gradio as gr 
from sentence_transformers import SentenceTransformer,util
import pickle 
import pandas as pd 
from huggingface_hub import hf_hub_download

pd.options.mode.chained_assignment = None  # Turn off SettingWithCopyWarning

songs_df = pd.read_csv(hf_hub_download('damilojohn/Personal_Playlist_Generator',repo_type='dataset',filename = 'spotify_transformed.csv'))
mappings = pd.read_csv(hf_hub_download('damilojohn/Personal_Playlist_Generator',repo_type='dataset',filename ='song_mappings.csv'))
verses_df = pd.read_csv(hf_hub_download('damilojohn/Personal_Playlist_Generator',repo_type='dataset',filename = 'verses.csv'))
song_embeddings = pickle.load(open(hf_hub_download('damilojohn/Personal_Playlist_Generator',repo_type='dataset',filename ='embeddings.pkl'),'rb'))
embedder = SentenceTransformer('msmarco-distilbert-base-v4')
verses_df.rename(columns={'0':'verse'},inplace=True)
mappings.rename(columns={'Unnamed: 0':'verse','0':'song_name'},inplace=True)


def generate_playlist(prompt):
  prompt_embed = embedder.encode(prompt)
  hits = util.semantic_search(prompt_embed,song_embeddings,top_k=30)
  hits = pd.DataFrame.from_dict(hits[0])
  verses_match = verses_df.iloc[hits['corpus_id']]
  songs_match = mappings[mappings['verse'].isin(verses_match['verse'].values)]
  songs_match = songs_df[songs_df['song_name'].isin(songs_match['song_name'].values)]
  songs_match = songs_match.sort_values('song_name')
  songs_match = songs_match.drop_duplicates(subset='song_name')
  songs_name = list(songs_match['song_name'])
  cover_art = list(songs_match['image'])
  images = [gr.Image.update(value=art,visible=True) for art in cover_art]
  return (
      gr.Radio.update(label='songs',interactive=True,choices=songs_name),
      *images
      )
  
  
def set_example_prompt(examples):
  return gr.TextArea.update(value=examples[0]) 
  
  
  
demo = gr.Blocks()
with demo:
  gr.Markdown(
      ''' 
      # A playlist Generator for Afrobeats
      This was built using Sentence Transformers and gradio

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
          components=[song_prompt],
          samples= [
              ['Lazy day'],
              ['I need money'],
              ['nobody gets me ']
          ]
      )
    with gr.Column():
      fetch_songs = gr.Button(value='generate your playlist',).style(full_width=True)
      with gr.Row():
                tile1 = gr.Image(value="https://i.imgur.com/bgCDfT1.jpg", show_label=False, visible=True)
                tile2 = gr.Image(value="https://i.imgur.com/bgCDfT1.jpg", show_label=False, visible=True)
                tile3 = gr.Image(value="https://i.imgur.com/bgCDfT1.jpg", show_label=False, visible=True)
      with gr.Row():
              tile4 = gr.Image(value="https://i.imgur.com/bgCDfT1.jpg", show_label=False, visible=True)
              tile5 = gr.Image(value="https://i.imgur.com/bgCDfT1.jpg", show_label=False, visible=True)
              tile6 = gr.Image(value="https://i.imgur.com/bgCDfT1.jpg", show_label=False, visible=True)
      with gr.Row():
              tile7 = gr.Image(value="https://i.imgur.com/bgCDfT1.jpg", show_label=False, visible=True)
              tile8 = gr.Image(value="https://i.imgur.com/bgCDfT1.jpg", show_label=False, visible=True)
              tile9 = gr.Image(value="https://i.imgur.com/bgCDfT1.jpg", show_label=False, visible=True)

      # Workaround because of the Gallery issues
      tiles = [tile1, tile2, tile3, tile4, tile5, tile6, tile7, tile8, tile9]

      with gr.Row():
        song_options = gr.Radio(label='songs',interactive=True,choices=None,type='value')
    with gr.Column():
      lyrics = gr.Textbox(label='lyrics',placeholder="select a song to see it's lyrics")

  
    fetch_songs.click(
        fn=generate_playlist,
        inputs=[song_prompt],
        outputs=[song_options,*tiles]
    )
    example_prompts.click(
        fn=set_example_prompt,
        inputs = [example_prompts],
        outputs = example_prompts.components
    )
  

  demo.launch(debug=True,share=True)
