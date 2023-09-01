def chunk_files(file_contents, limit):
    if not file_contents:
        return []

    chunks = [[]]
    current_size = 0
    for file_content in file_contents:
        if len(file_content) > limit:
            raise ValueError(
                f"File of size {len(file_content)} is bigger than limit of {limit}"
            )
        if current_size + len(file_content) > limit:
            chunks.append([])
            current_size = 0
        chunks[-1].append(file_content)
        current_size += len(file_content)
    return chunks
