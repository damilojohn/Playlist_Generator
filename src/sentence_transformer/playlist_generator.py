from sentence_transformers import SentenceTransformer, util
import argparse


class PlaylistGenerator:
    '''Loads Sentence Transformer and Generates Embeddings of input_text'''
    def __init__(self,):
        self.model_path = '/model/'
        self.model = SentenceTransformer(self.model_path)

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
        help='text describing your moodt'
    )
    args = parser.parse_args()
    embedder = PlaylistGenerator()
    embed = embedder.predict(args.input_text)
    print(embed)


if __name__ == '__main__':
    main()
