#
# Copyright © 2022-present Peter M. Stahl pemistahl@gmail.com
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

import time

from concurrent.futures import ProcessPoolExecutor
from lingua import LanguageDetectorBuilder

low_accuracy_detector = (
    LanguageDetectorBuilder.from_all_languages()
    .with_low_accuracy_mode()
    .with_preloaded_language_models()
    .build()
)
high_accuracy_detector = (
    LanguageDetectorBuilder.from_all_languages()
    .with_preloaded_language_models()
    .build()
)


def detect_with_low_accuracy(sentence):
    low_accuracy_detector.detect_language_of(sentence)


def detect_with_high_accuracy(sentence):
    return high_accuracy_detector.detect_language_of(sentence)


sentences = [
    "ربما يبتعد العقرب عن بعض الذين يخيبون أمله، أو يشعر بالحاجة إلى الانتقاء، وعدم البحث عن النشاطات التي ترهق أكثر مما تسعده.",
    "Επί της ουσίας τόσο οι υφιστάμενες ενισχύσεις που οφείλονται στους κτηνοτρόφους όσο και αυτές της νέας προγραμματικής περιόδου παραμένουν στον αέρα.",
    "It has three co-chairs, one from each of a provincial health and agriculture department, and a third from the federal government.",
    "અશ્વિની ભટ્ટની નવલકથામાંથી થોડુંક માણસ જ્યારે વેદનાની પરાકાષ્ટાની સીમા વટાવી જાય પછી એક એવી પરિસ્થિતિ આવે છે જ્યારે દર્દ-વેદના નથી રહેતી, વેદના છે કે નહિ તેનો પણ કોઇ ખ્યાલ નથી રહેતો.",
    "・京都大学施設に電離圏における電子数などの状況を取得可能なイオノゾンデ受信機（斜入射観測装置）を設置することで、新たな観測手法が地震先行現象検出に資するかを検証する。",
    "ამასთანავე წანარები სათავეში უდგებიან (თუ წარმართავენ?) კახეთის გაერთიანებისა და ერთიანი სამთავროს ჩამოყალიბების პროცესს.",
    "하지만 금융 전문가들은 “전체 대출 중 부동산 PF로의 쏠림 현상이 심각한 상태에서 각종 대출 규제로 자금 여력이 부족해질 경우 연체율이 높아질 수 있는데 당국이 안이하게 대응하는 측면이 있다”고 지적했다.",
    "И потому я должен возблагодарить провидение; если бы не провидение, то сердце твое, бедный сэр Пол, все конечно разбилось бы.",
    "ส.บัญชีรายชื่อ พรรคเพื่อไทย แต่อยู่ในระหว่างการตัดสินเรื่องการเป็นสมาชิกภาพของพรรคการเมือง เพราะถูกคุมขังโดยหมายศาล ระหว่างการสมัครรับเลือกตั้ง ซึ่งขณะนี้อยู่ในระหว่างการพิจารณาของ กกต.",
    "人们必须面对：遭受严重破坏的自然生态；大自然反扑所造成的天灾人祸；人口快速成长的沈重压力；生存竞争日异严峻的社会情况；传统家庭结构逐渐瓦解的隐忧，社会价值观念混淆等问题。",
] * 1000


def benchmark_language_detection_in_low_accuracy_mode():
    print("Detect language of 10,000 sentences in low accuracy mode...")
    start = time.perf_counter()

    for sentence in sentences:
        detect_with_low_accuracy(sentence)

    stop = time.perf_counter()
    print(f"Time: {stop - start:.2f} seconds")


def benchmark_language_detection_in_low_accuracy_mode_with_processes(n):
    print(
        f"Detect language of 10,000 sentences in low accuracy mode with {n} processes..."
    )
    start = time.perf_counter()

    with ProcessPoolExecutor(max_workers=n) as executor:
        executor.map(detect_with_low_accuracy, sentences)

    stop = time.perf_counter()
    print(f"Time: {stop - start:.2f} seconds")


def benchmark_language_detection_in_high_accuracy_mode():
    print("Detect language of 10,000 sentences in high accuracy mode...")
    start = time.perf_counter()

    for sentence in sentences:
        detect_with_high_accuracy(sentence)

    stop = time.perf_counter()
    print(f"Time: {stop - start:.2f} seconds")


def benchmark_language_detection_in_high_accuracy_mode_with_processes(n):
    print(
        f"Detect language of 10,000 sentences in high accuracy mode with {n} processes..."
    )
    start = time.perf_counter()

    with ProcessPoolExecutor(max_workers=n) as executor:
        executor.map(detect_with_high_accuracy, sentences)

    stop = time.perf_counter()
    print(f"Time: {stop - start:.2f} seconds")


def benchmark_preloading_all_language_models_in_low_accuracy_mode():
    print("Preload all language models in low accuracy mode...")
    high_accuracy_detector.unload_language_models()
    start = time.perf_counter()

    LanguageDetectorBuilder.from_all_languages().with_low_accuracy_mode().with_preloaded_language_models().build()

    stop = time.perf_counter()
    print(f"Time: {stop - start:.2f} seconds")


def benchmark_preloading_all_language_models_in_high_accuracy_mode():
    print("Preload all language models in high accuracy mode...")
    high_accuracy_detector.unload_language_models()
    start = time.perf_counter()

    LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build()

    stop = time.perf_counter()
    print(f"Time: {stop - start:.2f} seconds")


if __name__ == "__main__":
    benchmark_language_detection_in_low_accuracy_mode()
    print()
    benchmark_language_detection_in_low_accuracy_mode_with_processes(4)
    print()
    benchmark_language_detection_in_high_accuracy_mode()
    print()
    benchmark_language_detection_in_high_accuracy_mode_with_processes(4)
    print()
    benchmark_preloading_all_language_models_in_low_accuracy_mode()
    print()
    benchmark_preloading_all_language_models_in_high_accuracy_mode()
    print()
