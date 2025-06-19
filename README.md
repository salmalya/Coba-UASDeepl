# 🚀 RAG API HuggingFace

Proyek ini menggunakan **Retrieval-Augmented Generation (RAG)** dengan model dari [Hugging Face](https://huggingface.co).

---

## 📋 Persiapan / Requirement

1. **Buat virtual environment:**

    ```bash
    python -m venv rag-env
    ```

2. **Aktifkan virtual environment:**

    - **Windows:**

        ```bash
        rag-env\Scripts\activate
        ```

    - **Mac/Linux:**

        ```bash
        source rag-env/bin/activate
        ```

3. **Install dependencies dari `requirements.txt`:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Buat API key di** [huggingface.co](https://huggingface.co), lalu:
    - Tambahkan ke file `.env` pada root proyek seperti berikut:

    ```env
    HUGGINGFACEHUB_API_TOKEN=your_api_key_here
    ```

5. **(Khusus Windows)** Jalankan PowerShell sebagai Administrator dan jalankan:

    ```powershell
    Set-ExecutionPolicy RemoteSigned -Scope Process
    ```

6. **Jalankan server FastAPI:**

    ```bash
    uvicorn app.main:app --reload
    ```

---

## 🧪 Akses API

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Tampilan HTML (frontend):** [http://localhost:8000/](http://localhost:8000/)

---

## 💬 Contoh Pertanyaan

```text
"how many people work in Konstruksi sector in Februari 2024"
