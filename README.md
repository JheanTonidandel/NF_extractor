# 📄 Extrator de Dados de Notas Fiscais com Azure e OpenAI

Este projeto é uma ferramenta simples que utiliza o **Azure Document Intelligence** para leitura de documentos e o **OpenAI GPT-4o** para extração de campos relevantes de **notas fiscais**.

## ⚙️ Tecnologias Utilizadas

- Python 3
- Azure Document Intelligence
- Azure OpenAI (GPT-4o)
- requests
- dotenv

## 🧠 O que ele faz?

Dado um documento (PDF ou imagem) de nota fiscal:
1. Extrai o texto com Azure Document Intelligence.
2. Envia o conteúdo para o OpenAI.
3. Retorna campos estruturados como número da nota, chave de acesso, CNPJ, nome da empresa e destinatário.

## 🚀 Como usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/JheanTonidandel/NF_extractor
   cd NF_extractor
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Copie o `.env.example` para `.env` e preencha com suas chaves:
   ```bash
   cp .env.example .env
   ```

4. Coloque um arquivo `exemplo_nota.pdf` na pasta files do projeto.

5. Execute:
   ```bash
   python src/main.py
   ```

## 📦 Exemplo de Saída

```
Número da nota fiscal: 123456
Chave de acesso: 1234 5678 9123 ...
Data de emissão: 01/01/2024
CNPJ: 12.345.678/0001-99
Nome da empresa: Empresa Exemplo LTDA
Destinatário (CNPJ): 98.765.432/0001-88
Destinatário (Nome da empresa): Cliente Exemplo
```

## 🛡️ Segurança

- Nenhuma chave de API está presente no repositório.
- As credenciais devem ser configuradas via `.env`.

## 📄 Licença

Este projeto está licenciado sob a MIT License.
