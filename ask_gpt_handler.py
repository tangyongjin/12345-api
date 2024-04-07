import openai
import os

api_key = os.environ.get("OPENAI_API_KEY")


def ask_gpt(question, max_tokens=1000):

    # prompt12345 = f" 现在假设你是一个市政服务专家,我将给你一段文本,请给出分类,分类请从'经济调节','市场监管','社会管理','公共服务', '生态环境保护'这几项中选择一个最合适的,文本如下:{question},请直接给出某一项的分类,不需要其他的输出, 即:直接回答分类的结果"
    prompt12345 = (
        "现在假设你是一个市政CRM专家,我将给你一段文本,请给出分类,"
        "分类请从'市容环境','宣传广告','施工管理','街面秩序', '突发事件','其他事件'这几项中选择一个最合适的,"
        f"文本如下:{question},请直接给出某一项的分类,如果你无法确定分类,请给出'其他事件',不需要其他的输出, 即:直接回答分类的结果"
    )

    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt12345,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.2,
    )

    print("💬💬💬💬💬💬💬💬💬💬💬💬💬💬💬💬💬")
    print(response)

    """
    Completion(
        id="cmpl-9Anx7QvF1J2AsmPhoMvbioL11lUkb",
        choices=[
            CompletionChoice(
                finish_reason="stop", index=0, logprobs=None, text="\n\n公共服务"
            )
        ],
        created=1712362325,
        model="gpt-3.5-turbo-instruct",
        object="text_completion",
        system_fingerprint=None,
        usage=CompletionUsage(completion_tokens=4, prompt_tokens=123, total_tokens=127),
    )
    """

    return response
