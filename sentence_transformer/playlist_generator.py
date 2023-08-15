from sentence_transformers import SentenceTransformer, util
import argparse
import os
import wandb

os.environ['WANDB_API_KEY'] = '6078e9b1aed535c27c3f1179d4bcc048d3d95a66'


run = wandb.init()
artifact = run.use_artifact('damilojohn/Playlist Generator/Playlist-Generator-Sentence-Transformer:v0', type='model')
model_dir = artifact.download(root = "../../../tmp")
# Load your Hugging Face model from that folder
#  using the same model class


class PlaylistGenerator:
    '''Loads Sentence Transformer and Generates Embeddings of input_text'''
    def __init__(self,):
        self.model = SentenceTransformer(model_dir, device="cpu")
    def generate_embeds(self, text):
        self.embed = self.model.encode(text)
        return self.embed

    def generate_playlist(self, verse_embeddings):
        hits = util.semantic_search(self.embed, verse_embeddings, top_k=20)
        return hits


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_text',
        type=str,
        help='text describing your mood'
    )
    args = parser.parse_args()
    embedder = PlaylistGenerator()
    embed = embedder.generate_embeds(args.input_text)
    print(embed)


if __name__ == '__main__':
    main()
