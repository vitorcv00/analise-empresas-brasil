# Bridge

Esta pasta vai concentrar a ponte entre a interface desktop e o backend atual.

Responsabilidades esperadas:
- executar a coleta por ticker
- listar arquivos gerados
- carregar favoritos
- expor operacoes simples para a UI

Exemplo de fluxo:
1. UI envia ticker
2. bridge chama o backend
3. bridge devolve status, arquivos e caminhos locais
