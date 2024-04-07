from ollama import Client


def ask_ollama(question):

    client = Client(host="http://119.255.238.247:11434")
    llm = "gemma"
    prompt12345 = (
        "现在假设你是一个市政CRM专家,我将给你一段文本,请给出分类,"
        "分类只能从'市容环境','宣传广告','施工管理','街面秩序', '突发事件','其他事件'这6项中选择一个最合适的,"
        f"文本如下:{question},请你简洁的直接给出分类,如果你无法确定分类,请回答'其他事件',不需要你做任何说明"
    )

    response = client.generate(
        model=llm,
        prompt=prompt12345,
        stream=False,
    )
    print(response)
    return "市容环境"
    # return response["message"]["content"]
