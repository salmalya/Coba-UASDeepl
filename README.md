# 🚀 RAG API HuggingFace

Proyek ini menggunakan **Retrieval-Augmented Generation (RAG)** dengan model dari [Hugging Face](https://huggingface.co).

---

## 📋 Persiapan / Requirement

1. **Buat API key** di situs [huggingface.co](https://huggingface.co)
2. **Salin API key** ke file `.env`
3. **Jalankan backend** menggunakan PowerShell (Run as Administrator), lalu jalankan perintah berikut dari direktori root proyek:

    ```powershell
    Set-ExecutionPolicy RemoteSigned -Scope Process
    .\rag-env\Scripts\activate
    uvicorn app.main:app --reload
    ```

---

## 🧪 Akses API

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Tampilan HTML:** [http://localhost:8000/](http://localhost:8000/)

---

## 💬 Contoh Pertanyaan

"how many people work in Konstruksi sector in Februari 2024"

---
