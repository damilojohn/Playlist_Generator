from sentence_transformers import SentenceTransformer, util
import argparse
import wandb 


with wandb.init(project="Text Descrambling") as run:

    # Connect an Artifact to the run
    model_name = run.use_artifact('damilojohn/Playlist Generator/Playlist-Generator-Sentence-Transformer:v0',
                                  type='model')
    model_artifact = run.use_artifact(model_name)

    # Download model weights to a folder and return the path
    model_dir = model_artifact.download()

    # Load your Hugging Face model from that folder
    #  using the same model class
    model = SentenceTransformer(
        model_dir, )


class PlaylistGenerator:
    '''Loads Sentence Transformer and Generates Embeddings of input_text'''
    def __init__(self,):
        self.model = model 

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
    embed = embedder.predict(args.input_text)
    print(embed)


if __name__ == '__main__':
    main()
