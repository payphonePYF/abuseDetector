import streamlit as st
from matplotlib import pyplot as plt

import sparkAPI
def main():
    st.title('骂人检测应用')

    # 显示输入框，让用户输入20条句子
    sentences = st.text_area('请输入句子（20句或任意数量），每行一个', height=200)

    if st.button('开始检测'):
        if len(sentences)>0:
            # 按钮点击后执行检测
            st.write(f"正在检测请稍等")
            results = detect_abuse(sentences.split('\n'))
            show_results(results)
        else:
            st.write(f"内容不能为空")
def detect_abuse(sentences):
    # 使用星火或文心一言的接口对每个句子进行骂人检测
    sparkAPI.latest_message_content = []
    new_sentences = sentences.copy()
    for j,sentence in enumerate(sentences):
        # query = sentence + "是不是在侮辱人？你只回答是或不是"
        # st.write(f" {len(sentence)}: {sentence}")
        if len(sentence) > 0:
            # st.write(f"问问星火: {sentence}")
            sparkAPI.xinghuo(
                appid="870c51cc",
                api_secret="YjE3M2YxYTIyNDBiMzcwZDI2NzU1MmI4",
                api_key="f75fa9778971ebea5566505b72fc2d88",
                gpt_url="wss://spark-api.xf-yun.com/v3.5/chat",
                domain="generalv3.5",
                query=sentence + " 这句话是不是在侮辱人？你只回答是或不是"
            )
        else:
            # st.write(f" 删除句子: {sentence}")
            new_sentences.remove(sentence)
            # st.write(f"删除后的sentences: {new_sentences}")
            # st.write(f"删除后的sentences: {sparkAPI.latest_message_content}")

    # st.write(f"所有cnotent: {sparkAPI.latest_message_content}")
    # 在此编写调用检测接口的代码，以及返回结果的逻辑
    results = {'句子{}--{}'.format(i+1,sentence): '是骂人' if is_abusive(sparkAPI.latest_message_content[i]) else '不是骂人' for i, sentence in enumerate(new_sentences)}
    return results
abuse_num =0
not_abuse_num =0
def is_abusive(content):

    global not_abuse_num
    global abuse_num
    # 这里填写调用骂人检测接口的逻辑
    if "不" in content:
        # st.write(f"Query for sentence: {content}不是侮辱人")
        not_abuse_num += 1
        return False
    # 返回 True 或 False 表示是否骂人
    # st.write(f"Query for sentence: {content}是侮辱人")
    abuse_num += 1
    return True  # 示例，需要替换成实际调用接口的代码

def show_results(results):
    # 显示检测结果
    st.header('检测结果统计')
    for sentence, result in results.items():
        st.write(f'{sentence}: {result}')

    # 绘制柱状图
    fig, ax = plt.subplots()
    categories = ['abuse', 'not abuse']
    counts = [abuse_num, not_abuse_num]

    ax.bar(categories, counts)

    # 设置图表标题和标签
    ax.set_title('statistic')
    ax.set_xlabel('abuse or not')
    ax.set_ylabel('num of sentence')

    # 在 Streamlit 中显示图表
    st.pyplot(fig)

if __name__ == '__main__':
    main()
