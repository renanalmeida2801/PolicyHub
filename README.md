# PolicyHub

**PolicyHub** é um serviço reutilizável de políticas de acesso, projetado para centralizar a avaliação de permissões, gerenciamento de regras de acesso e auditoria de decisões em sistemas distribuídos.

## Funcionalidades

* **Avaliação de Políticas**: Verifica permissões baseadas em atributos (ABAC), considerando usuário, papéis (*roles*), ação, recurso e contexto.
* **Gerenciamento de Políticas (CRUD)**: API para criar, listar, atualizar e remover definições de políticas dinamicamente.
* **Auditoria**: Registro automático de todas as tentativas de acesso e modificações de políticas para rastreabilidade.
* **Resiliência**: Implementação do padrão **Circuit Breaker** para proteger o serviço contra falhas em cascata durante a avaliação de políticas e do padrão **Retry** que permite a repetição controlada de operações que falham temporariamente.

## Exemplo de Uso

Para verificar se um usuário tem permissão para realizar uma ação, envie uma requisição `POST` para o endpoint `/evaluate`.

**Endpoint:** `POST /evaluate`

**Payload (JSON):**

```json
{
  "user": {
    "id": "user123",
    "roles": ["aluno"]
  },
  "action": "SUBMETER_PROJETO",
  "resource": "PROJETO",
  "context": {
    "prazo_expirado": false
  }
}
```
**Resposta:**

```json
{
  "decision": "PERMIT"
}
```

## Endpoints Principais

| Método | Endpoint                  | Descrição                                                        |
|--------|---------------------------|------------------------------------------------------------------|
| POST   | `/evaluate`               | Avalia uma requisição de acesso com base nas políticas           |
| GET    | `/policies`               | Lista todas as políticas cadastradas                             |
| POST   | `/policies`               | Cria uma nova política de acesso                                 |
| GET    | `/policies/{policy_name}` | Obtém detalhes de uma política específica                        |
| PUT    | `/policies/{policy_name}` | Atualiza uma política existente                                  |
| DELETE | `/policies/{policy_name}` | Remove uma política                                              |
| GET    | `/audit/logs`             | Retorna os logs de auditoria do sistema                           |

##  Arquitetura

### Camada de Entrada (API)
- Receber requisições HTTP e validar os dados de entrada.

### Camada de Avaliação (Core)
- Avaliar as políticas de acesso e decidir se a operação é permitida ou negada.

### Camada de Proteção (Resiliência)
- Monitorar falhas e impedir o processamento de requisições em momentos de instabilidade.

### Camada de Persistência e Auditoria
- Armazenar as políticas de acesso e registrar as decisões e alterações realizadas.


## Como Rodar

### Instalar dependências
```bash
pip install -r requirements.txt
```

### Executar o servidor
```bash
uvicorn app.main:app --reload
```

### Acessar a documentação
Link: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Autores
- Antonio Herik Cosmo Martins - 516098
- Renan Victor de Almeida Silva - 538428
 

