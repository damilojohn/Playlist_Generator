from sentence_transformers import SentenceTransformer, util
import argparse
import os


# Load your Hugging Face model from that folder
#  using the same model class


class PlaylistGenerator:
    '''Loads Sentence Transformer and Generates Embeddings of input_text'''
    def __init__(self,):
        self.model = SentenceTransformer('msmarco-distilbert-base-v4', device="cpu",)

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
