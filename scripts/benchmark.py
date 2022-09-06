#
# Copyright © 2022 Peter M. Stahl pemistahl@gmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either expressed or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import timeit


def benchmark_preloading_all_language_models_in_low_accuracy_mode():
    setup = "from lingua import LanguageDetectorBuilder"
    stmt = """LanguageDetectorBuilder\
        .from_all_languages()\
        .with_low_accuracy_mode()\
        .with_preloaded_language_models()\
        .build()"""

    print("Measuring time to preload all language models in low accuracy mode...")
    result = timeit.timeit(setup=setup, stmt=stmt, number=1)
    print(f"Time: {result:.2f} seconds")


def benchmark_preloading_all_language_models_in_high_accuracy_mode():
    setup = "from lingua import LanguageDetectorBuilder"
    stmt = """LanguageDetectorBuilder\
        .from_all_languages()\
        .with_preloaded_language_models()\
        .build()"""

    print("Measuring time to preload all language models in high accuracy mode...")
    result = timeit.timeit(setup=setup, stmt=stmt, number=1)
    print(f"Time: {result:.2f} seconds")


def benchmark_language_detection():
    setup = (
        "from lingua import LanguageDetectorBuilder\n"
        "detector = LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build()\n"
        "sentences = ("
        "'ربما يبتعد العقرب عن بعض الذين يخيبون أمله، أو يشعر بالحاجة إلى الانتقاء، وعدم البحث عن النشاطات التي ترهق أكثر مما تسعده.',"
        "'Επί της ουσίας τόσο οι υφιστάμενες ενισχύσεις που οφείλονται στους κτηνοτρόφους όσο και αυτές της νέας προγραμματικής περιόδου παραμένουν στον αέρα.',"
        "'It has three co-chairs, one from each of a provincial health and agriculture department, and a third from the federal government.',"
        "'અશ્વિની ભટ્ટની નવલકથામાંથી થોડુંક માણસ જ્યારે વેદનાની પરાકાષ્ટાની સીમા વટાવી જાય પછી એક એવી પરિસ્થિતિ આવે છે જ્યારે દર્દ-વેદના નથી રહેતી, વેદના છે કે નહિ તેનો પણ કોઇ ખ્યાલ નથી રહેતો.',"
        "'・京都大学施設に電離圏における電子数などの状況を取得可能なイオノゾンデ受信機（斜入射観測装置）を設置することで、新たな観測手法が地震先行現象検出に資するかを検証する。',"
        "'ამასთანავე წანარები სათავეში უდგებიან (თუ წარმართავენ?) კახეთის გაერთიანებისა და ერთიანი სამთავროს ჩამოყალიბების პროცესს.',"
        "'하지만 금융 전문가들은 “전체 대출 중 부동산 PF로의 쏠림 현상이 심각한 상태에서 각종 대출 규제로 자금 여력이 부족해질 경우 연체율이 높아질 수 있는데 당국이 안이하게 대응하는 측면이 있다”고 지적했다.',"
        "'И потому я должен возблагодарить провидение; если бы не провидение, то сердце твое, бедный сэр Пол, все конечно разбилось бы.',"
        "'ส.บัญชีรายชื่อ พรรคเพื่อไทย แต่อยู่ในระหว่างการตัดสินเรื่องการเป็นสมาชิกภาพของพรรคการเมือง เพราะถูกคุมขังโดยหมายศาล ระหว่างการสมัครรับเลือกตั้ง ซึ่งขณะนี้อยู่ในระหว่างการพิจารณาของ กกต.',"
        "'人们必须面对：遭受严重破坏的自然生态；大自然反扑所造成的天灾人祸；人口快速成长的沈重压力；生存竞争日异严峻的社会情况；传统家庭结构逐渐瓦解的隐忧，社会价值观念混淆等问题。'"
        ")"
    )
    stmt = "for sentence in sentences: detector.detect_language_of(sentence)"

    print(
        "Measuring time to detect language of 10,000 sentences after preloading all models..."
    )
    result = timeit.timeit(setup=setup, stmt=stmt, number=1000)
    print(f"Time: {result:.2f} seconds")


if __name__ == "__main__":
    benchmark_preloading_all_language_models_in_low_accuracy_mode()
    print()
    benchmark_preloading_all_language_models_in_high_accuracy_mode()
    print()
    benchmark_language_detection()
    print()
