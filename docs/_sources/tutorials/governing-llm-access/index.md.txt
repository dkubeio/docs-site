# Governing LLM Access

SecureLLM is the gateway every request to a language model passes through on DKubeX. These tutorials
walk you through the three things you do to put a model safely in front of your users: connect the
providers whose models you want to serve, hand out scoped API keys that control who can call them,
and attach guardrail policies that screen prompts and responses before they reach anyone.

Start here if you're setting up model access for a team or tightening the controls around an existing
deployment.

```{toctree}
:maxdepth: 1

configuring-and-enabling-ai-providers-in-securellm
creating-and-using-api-keys-in-securellm
testing-and-deploying-guardrail-policies-in-securellm
```
