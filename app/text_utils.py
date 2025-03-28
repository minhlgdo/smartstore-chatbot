# Utility functions for text processing


def clean_text(text: str) -> str:
    res = text.replace("""

위 도움말이 도움이 되었나요?


별점1점

별점2점

별점3점

별점4점

별점5점



소중한 의견을 남겨주시면 보완하도록 노력하겠습니다.

보내기""", "")
    res = res.replace("도움말 닫기", "")

    return res

def sliding_window_split_text(text: str, chunk_size=1000, chunk_overlap=200) -> list[str]:
    '''
    Splits the text into chunks of specified size with a specified overlap.
    '''
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        # If the remaining words are less than window_size, break.
        if i + chunk_size >= len(words):
            break
        i += chunk_size - chunk_overlap
    return chunks
