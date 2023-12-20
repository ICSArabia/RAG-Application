from .helper import load_document, chunk_data, create_embeddings

def create_and_save_embeddings(source_file_path, progress_callback=None):

    def report_progress(percentage):
        if progress_callback:
            progress_callback(percentage)
    
    total_progress = 0

    data = load_document(source_file_path)
    loading_progress = 40
    total_progress += loading_progress
    report_progress(total_progress)

    chunks = chunk_data(data)
    chunking_progress = 20
    total_progress += chunking_progress
    report_progress(total_progress)

    vector_store = create_embeddings(chunks, file_name=source_file_path)
    embedding_progress = 40
    total_progress += embedding_progress
    report_progress(total_progress)


