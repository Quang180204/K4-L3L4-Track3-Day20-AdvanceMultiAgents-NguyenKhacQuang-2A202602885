# Báo cáo Lab: Self evolving Agentic

> Sao chép tệp này thành `report/REPORT.md` (đã làm ở Phần 0) và điền dần qua các Phần của lab. Xóa các dòng hướng dẫn dạng trích dẫn (bắt đầu bằng `>`). Văn phong kỹ thuật, ngắn gọn, mọi nhận định đi kèm số liệu hoặc bằng chứng. Trong buổi học: điền mục 1 đến 7 (bản nháp). Sau buổi học: hoàn thiện mục 8 đến 10.

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Nguyễn Khắc Quang | 2A202602885 | 100% |

- Mô hình: `gemini-3.5-flash-lite` (qua provider `langchain-google-genai` / `google_genai:gemini-3.5-flash-lite`), nhiệt độ: `0`, `recursion_limit`: `60`
- Phiên bản Deep Agents: `deepagents==0.7.21`, hệ điều hành: Ubuntu 26.04 LTS (WSL2 trên Windows 11), chạy trực tiếp trong WSL
- Số lần chạy tác vụ đã dùng / ngân sách:
- Commit của tag `freeze`:


## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

- H1 (subagents so với baseline): Dự đoán điểm trung bình của `subagents` trên tác vụ đánh giá sẽ tương đương hoặc chỉ tăng nhẹ so với `baseline` (chênh lệch ≤ +0.05 điểm), nhưng tổng token tiêu thụ sẽ tăng đáng kể từ 40% đến 80%. Căn cứ: Phân loại lỗi ở mục 4 cho thấy 100% check kỹ thuật (A-D) đã đạt ở baseline, trong khi toàn bộ lỗi thất bại thuộc nhóm E (quy ước tổ chức `rule_` không có trong đề). Việc chia nhỏ công việc cho các subagent chuyên biệt (`explorer`, `implementer`, `reviewer`) chỉ cải thiện độ tin cậy thực thi kỹ thuật nhưng không thể cung cấp tri thức về các quy ước ẩn của tổ chức; đồng thời mỗi lời gọi subagent là vô trạng thái (stateless) đòi hỏi truyền lại ngữ cảnh, làm tăng chi phí phối hợp (coordination overhead) theo các nghiên cứu về đa tác tử (ví dụ SWE-bench / AutoGen).
- H2 (skills-auto so với baseline): Dự đoán `skills-auto` sẽ đạt điểm cao nhất trên tác vụ đánh giá (dự kiến đạt từ 0.75 đến 0.85, cao hơn baseline khoảng +0.15 đến +0.25 điểm), với chi phí token gia tăng rất ít so với subagents. Căn cứ: Curator đã chiết xuất thành công các quy chuẩn thủ tục cốt lõi từ phản hồi `RULE:` của tác vụ học thành các skill trong `skills/auto/` (`enforce-type-hints-and-documentation` và `rigorous-output-formatting-and-schema`). Vì các tác vụ đánh giá trong cùng họ tái sử dụng các quy ước tổ chức này (theo thiết kế ở README mục 2.2), cơ chế nạp dần (progressive disclosure) của Deep Agents sẽ tiêm đúng tri thức thủ tục vào context đúng thời điểm, giúp tác tử tuân thủ quy ước mà không gây bùng nổ token.
- H3 (tác vụ học so với tác vụ đánh giá): Dự đoán điểm của cả ba điều kiện trên tác vụ đánh giá sẽ thấp hơn so với tác vụ học tương ứng (khoảng giảm dự kiến từ 0.05 đến 0.15 điểm), đặc biệt ở các check quy ước mới. Căn cứ: Thiết kế thí nghiệm nêu rõ mỗi tác vụ đánh giá bổ sung ít nhất một quy ước tổ chức mới mà tập học chưa từng gặp và dùng tập dữ liệu mới với các ca biên khác biệt. Do skill tự sinh bị đóng băng (freeze) và chỉ phản ánh các quy tắc đã học ở tập học, tác tử không thể phòng ngừa các quy ước mới này, dẫn đến hiện tượng suy giảm hiệu năng do dịch chuyển phân phối nhiệm vụ (task distribution shift).

## 3. Làm quen Deep Agents (Phần 0.3)

1. Tác tử mặc định có 9 công cụ: công cụ thao tác tệp (`ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`), shell (`execute`), và subagent (`task`). Trong đó, công cụ duy nhất cho phép chạy lệnh shell là `execute`.
2. Mô tả của công cụ `task` nói rằng subagent `general-purpose` dùng để nghiên cứu các câu hỏi phức tạp, tìm kiếm tệp/nội dung và thực thi tác vụ nhiều bước; subagent này có quyền truy cập toàn bộ công cụ như tác tử chính. Về ngữ cảnh: mỗi lần gọi subagent là vô trạng thái (stateless by default), subagent chỉ nhìn thấy nội dung prompt mà tác tử chính gửi cho nó và trả về một báo cáo duy nhất, không nhìn thấy lịch sử hội thoại trước đó của tác tử chính.
3. 
   - Trích dẫn hướng dẫn hành vi từ mô tả công cụ `task`: *"Each invocation is stateless by default: the agent sees only the prompt you give it and returns a single final report. Put full detail in the prompt and state exactly what it should return — unless an agent type below says it inherits your conversation instead."*
   - Trích dẫn hướng dẫn hành vi từ mô tả công cụ `execute`: *"You MUST avoid using search commands like find and grep. Instead use the grep, glob tools to search. Use read_file rather than cat/head/tail."*


## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

Bảng phân loại lỗi trên các lần chạy của tác vụ học (`baseline`):

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| `code-learn` | `tests_not_modified` | G (Sửa đổi tệp cấm) | `the original files in tests/ must not be modified (new test files are allowed)` (Tác tử sửa file `tests/test_report.py` trong quá trình sửa lỗi). |
| `code-learn` | `rule_type_hints` | E (Quy ước tổ chức) | `RULE: every public function (name not starting with '_') in the package has type annotations on all parameters and on the return value.` |
| `code-learn` | `rule_regression_tests` | E (Quy ước tổ chức) | `RULE: add tests/test_regressions.py with one test function per bug you fixed (at least 3); the file must pass.` |
| `code-learn` | `rule_changelog` | E (Quy ước tổ chức) | `RULE: record each fix in CHANGELOG.md under the heading '## Unreleased' as a bullet '- fix(<function name>): <short description>' (at least 3 bullets).` |
| `data-learn` | `rule_money_in_cents` | E (Quy ước tổ chức) | `RULE: money values in answer.json are integer cents (1606.67 USD is written 160667).` |
| `data-learn` | `rule_meta_block` | E (Quy ước tổ chức) | `RULE: answer.json has an object meta = {"source": <input file name>, "rows_in": <number of data rows>, "rows_used": <number of distinct orders with a known amount>}.` |
| `data-learn` | `rule_clean_csv` | E (Quy ước tổ chức) | `RULE: write workspace/clean.csv with the header order_id,timestamp_utc,region,amount_cents; one row per distinct order with a known amount; timestamp_utc as YYYY-MM-DDTHH:MM:SSZ (UTC); region in canonical spelling (North, South, East, West); amount in integer cents.` |
| `logs-learn` | `rule_service_names` | E (Quy ước tổ chức) | `RULE: service names in the output are lower-case with '-' replaced by '_' (payment-service -> payment_service).` |
| `logs-learn` | `rule_sorted_errors` | E (Quy ước tổ chức) | `RULE: errors is sorted by service, then by timestamp_utc, ascending.` |
| `logs-learn` | `rule_schema_header` | E (Quy ước tổ chức) | `RULE: the top-level object has "schema_version": 2 and "generated_by": "log-triage".` |

**Nhận xét:**
- **Nhóm lỗi chiếm đa số:** Nhóm **E (Vi phạm quy ước tổ chức)** chiếm tuyệt đối 9/10 lỗi thất bại (90%). Các quy ước này không được nêu rõ trong đề bài ban đầu của người dùng mà là quy chuẩn nội bộ của tổ chức (Acme conventions) được bot review kiểm tra sau đó.
- **Bằng chứng phủ định cho Nhóm A đến D:** Toàn bộ 17/17 check kỹ thuật chức năng (A-D) đều đạt điểm tuyệt đối: 6/6 ở `code-learn` (vượt qua test tính giá, discount nửa lên, phân loại stock, trích dẫn CSV RFC 4180), 5/5 ở `data-learn` (tính doanh thu Q1, số lượng đơn, top region, xử lý -999, khử trùng dòng), và 6/6 ở `logs-learn` (cấu trúc log, chuẩn hóa timestamp UTC, trích xuất exception traceback, tính repeat count, tổng hợp service count). Điều này chứng minh mô hình nền tảng (`gemini-3.5-flash-lite`) có năng lực suy luận và lập trình cốt lõi rất mạnh.
- **Khả năng phòng ngừa của Skill:** Skill hoàn toàn có thể phòng ngừa được Nhóm E một cách hiệu quả. Do Nhóm E là các tri thức thủ tục (procedural knowledge) mang tính quy chuẩn lặp lại, việc curator tổng hợp các quy tắc `RULE:` thành checklist trong `SKILL.md` sẽ giúp tác tử nạp vào context và tuân thủ chặt chẽ trước khi xuất kết quả.

## 5. Điều kiện `subagents` (Phần 2.3)

- **Các subagent đã định nghĩa (tên, vai trò, lý do thiết kế):**
  1. `explorer`: Tác tử con chuyên trách khám phá (read-only). Được cấp các công cụ `ls`, `read_file`, `glob`, `grep`. Lý do thiết kế: Cô lập bước khảo sát cấu trúc thư mục, lược đồ tệp, docstring và dữ liệu thô mà không lo vô tình làm biến đổi tệp hay chạy lệnh phá hủy môi trường.
  2. `implementer`: Tác tử con chuyên trách sửa đổi và thực thi. Được cấp toàn bộ công cụ thao tác tệp và shell `execute`. Lý do thiết kế: Tập trung cao độ vào việc viết mã xử lý, sửa lỗi bug cụ thể, và sinh dữ liệu kết quả theo chỉ đạo của tác tử chính.
  3. `reviewer`: Tác tử con thẩm định chất lượng. Được cấp công cụ đọc và chạy test `execute` (không có quyền ghi). Lý do thiết kế: Độc lập kiểm tra lại mã nguồn đã sửa, chạy suite kiểm thử, đối chiếu định dạng đầu ra với các quy chuẩn trước khi tác tử chính kết luận hoàn thành.

- **`subagent_calls` ở từng tác vụ và nhận xét (kể cả trường hợp bằng 0):**
  - `code-learn`: 5 lần gọi subagent (trong tổng số 12 tool calls). Tác tử chính chủ động phân quyền: gọi `explorer` (2 lần) để quét cấu trúc package và docstring, gọi `implementer` (2 lần) để chạy thử nghiệm và sửa code theo docstring, gọi `reviewer` để kiểm chứng suite test.
  - `data-learn`: 1 lần gọi subagent (`explorer`) để kiểm tra cấu trúc file `sales.csv` và các dạng format dữ liệu trước khi tác tử chính tự viết script xử lý và tính toán.
  - `logs-learn`: 1 lần gọi subagent (`explorer`) để đọc mẫu các dòng log, regex nhận dạng traceback và repeat counts trong `app.log`.
  - **Nhận xét chung:** Tác tử chính nhận biết rõ các vai trò của từng subagent thông qua `description` và có xu hướng giao việc mạnh mẽ nhất ở bài toán phức tạp nhiều module (`code-learn`), trong khi với các tác vụ xử lý tệp đơn lẻ (`data-learn`, `logs-learn`), tác tử chính chỉ gọi `explorer` ở giai đoạn đầu rồi tự hoàn thành phần còn lại.

- **Thông tin thiếu hoặc thừa khi giao việc (nếu có giao việc):**
  - Tác tử chính cung cấp prompt giao việc rất chi tiết: nêu rõ đường dẫn tương đối (`workspace/...`), mục tiêu khảo sát, các hàm cần đối chiếu docstring và yêu cầu báo cáo kết quả cụ thể mà không làm biến đổi môi trường.
  - Các subagent trả về báo cáo chất lượng cao, nêu chính xác các bất thường (ví dụ: `parse_price` thiếu xử lý dấu phẩy và ngoặc đơn kế toán, `apply_discount` dùng sai kiểu làm tròn). Tác tử chính đọc kỹ báo cáo và dựa vào đó để triển khai các bước tiếp theo.

- **Ảnh hưởng đến token và thời gian:**
  - **Token tiêu thụ tăng mạnh:** Tổng token cho cả 3 tác vụ học tăng từ 424,600 tokens (ở baseline) lên 1,150,656 tokens (tăng +171.0%). Cụ thể: `code-learn` tăng từ 143k lên 315k (+120%), `data-learn` tăng từ 212k lên 540k (+154%), `logs-learn` tăng từ 69k lên 295k (+327%).
  - **Thời gian thực thi kéo dài:** Chi phí phối hợp đa tác tử (stateless context passing) cộng với việc mỗi lời gọi subagent đều sinh chuỗi suy luận riêng biệt khiến thời gian chạy tăng gấp nhiều lần (`code-learn` mất 2307s, `data-learn` mất 668s, `logs-learn` mất 437s).
  - **Hiệu quả điểm số:** Điểm số không thay đổi so với baseline (`code-learn`: 6/10, `data-learn`: 5/8, `logs-learn`: 6/9). Điều này chứng minh đa tác tử cải thiện tính mạch lạc trong thực thi kỹ thuật nhưng không giúp tác tử tự phát hiện ra các quy ước ẩn của tổ chức (`rule_`).

## 6. Self-evolving: skill do curator sinh (Phần 3)

- **Số lần chạy curator, số skill bị xóa và lý do:**
  - Số lần chạy curator: 1 lần duy nhất (`python -m lab.curator`).
  - Số skill bị xóa hoặc chạy lại: 0 skill. Cả hai skill do curator sinh ra đều vượt qua bộ kiểm tra định dạng và an toàn (`validate_skill`), đảm bảo chuẩn YAML frontmatter, không chứa ký tự cấm, không vượt quá độ dài quy định và không đề cập bất kỳ định danh hay dữ liệu nào của tập đánh giá (`eval_markers`).
  - Nội dung các skill được giữ nguyên vẹn 100% từ đầu ra của curator, tuân thủ nguyên tắc tác tử tự tiến hóa (không sửa đổi thủ công).

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| `enforce-type-hints-and-documentation` | **Tổng quát:** Hướng dẫn thêm type hint cho mọi hàm public (không bắt đầu bằng `_`), bổ sung regression tests (`tests/test_regressions.py`), cập nhật `CHANGELOG.md` dưới tiêu đề `## Unreleased` và cấm sửa các test có sẵn trong `tests/`. Hoàn toàn không chứa tên hàm, biến cụ thể hay logic riêng của `code-learn`. | **Đúng hoàn toàn:** Hướng dẫn mạch lạc, chuẩn xác theo các quy ước kỹ nghệ phần mềm của Python và Acme, không chứa chỉ dẫn độc hại. | 8 dòng (thân 4 dòng). Description: *"Use this skill when writing or fixing Python packages and modules to ensure all public functions have complete type annotations and all requirements are met."* Phản ánh chính xác tình huống kích hoạt khi làm việc với module/package Python. |
| `rigorous-output-formatting-and-schema` | **Tổng quát:** Quy định chuẩn hóa định dạng tệp dữ liệu có cấu trúc (JSON/CSV): kiểm tra khóa cấp cao (`schema_version`, `generated_by`, `meta`), chuyển đổi tiền tệ sang cents nguyên, chuẩn hóa timestamp ISO 8601 UTC kết thúc bằng `Z`, chuẩn hóa tên thực thể (thay `-` bằng `_`), sắp xếp mảng theo khóa chính/phụ. | **Đúng hoàn toàn:** Khắc phục chính xác các lỗi thiếu sót cấu trúc định dạng từ `data-learn` và `logs-learn`. | 9 dòng (thân 5 dòng). Description: *"Use this skill when generating structured output files like JSON or CSV to ensure all field names, formats, units, and headers strictly match specifications."* Kích hoạt chuẩn xác khi xuất file JSON/CSV. |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

> Dán nội dung `report/table.md` và kết quả `python scripts/check_breakdown.py`. Nêu các lần chạy có `error` hoặc `skills_modified = true` (nếu có) và cách xử lý.

```text
(dán bảng ở đây)
```

## 8. Phân tích

> Trả lời từng câu bằng số liệu từ mục 7 và bằng chứng từ vết. Kết quả âm hoặc không có khác biệt vẫn hợp lệ nếu được phân tích tốt.

1. So với `baseline`, điều kiện nào cải thiện điểm tác vụ **học**? Điều kiện nào cải thiện điểm tác vụ **đánh giá**? Có điều kiện nào cải thiện tác vụ học nhưng không cải thiện tác vụ đánh giá? Nếu có, đó là dấu hiệu gì?
2. Tách điểm thành check kỹ thuật và check quy ước (`rule_`). Skill do curator sinh giúp nhóm check nào? Check quy ước **mới** của tác vụ đánh giá có được skill giúp không, và vì sao?
3. Dựa vào vết và `skills_read`, giải thích một check mà skill giúp đạt và một check mà skill không giúp (skill chưa được đọc, đọc nhưng không làm theo, skill thiếu hoặc sai).
4. Chi phí: so sánh số token trung bình giữa các điều kiện. Điều kiện nào có hiệu quả tốt nhất theo điểm trên mỗi token? Đa tác tử có đáng chi phí trong thí nghiệm này không?
5. Có dấu hiệu rò rỉ dữ liệu hoặc quá khớp nào trong skill sinh ra không? Nhóm đã phòng tránh như thế nào?
6. Nhiễu: so sánh điểm tác vụ học của cùng bộ skill ở Phần 3.4 (đã sao lưu) và sau đóng băng. Chênh lệch bao nhiêu? Nó cho biết điều gì về độ tin cậy của các chênh lệch trong bảng ở mục 7?

## 9. Hạn chế và tính hợp lệ

1. **Quy mô tập tác vụ còn nhỏ (3 tác vụ học và 3 tác vụ đánh giá):** Với mỗi họ bài toán (`code`, `data`, `logs`) chỉ có đúng 1 tác vụ học và 1 tác vụ đánh giá, kích thước mẫu thử nghiệm (sample size = 6) là tương đối hạn chế. Do đó, các kết luận về hiệu quả tổng quát hóa của skill có biên độ dao động lớn và chịu ảnh hưởng đáng kể bởi đặc thù của từng đề bài cụ thể.
2. **Thí nghiệm đơn lần chạy (single-run evaluation) và nhiễu mô hình:** Mặc dù đã cấu hình nhiệt độ (temperature) = 0, việc gọi công cụ (tool calling), thứ tự sinh token và cơ chế phân nhánh của đa tác tử vẫn tồn tại tính phi xác định nhất định. Việc chỉ đo đạc một lần chạy duy nhất cho mỗi điều kiện khiến việc phân tách rạch ròi giữa "hiệu quả học thực sự" và "nhiễu ngẫu nhiên" (random variance) gặp thách thức.
3. **Quy ước tổ chức mang tính thiết kế sẵn (synthetic benchmark conventions):** Các quy chuẩn trong bài lab (định dạng `meta`, `clean.csv`, tiền tệ tính theo cents, `schema_version`, v.v.) được thiết kế nhân tạo theo khuôn mẫu của tổ chức giả lập Acme. Mặc dù phản ánh tốt tri thức thủ tục (procedural rules), độ phức tạp này chưa bao quát hết toàn bộ các tình huống công nghệ phức tạp trong các kho mã nguồn thực tế.
4. **Giới hạn trên một kiến trúc mô hình duy nhất (`gemini-3.5-flash-lite`):** Toàn bộ thí nghiệm được thực hiện trên một mô hình nền tảng. Khả năng nhạy bén ngữ cảnh đối với system prompt, thói quen đọc `SKILL.md` nạp dần và xu hướng điều phối qua subagent có thể biểu hiện rất khác biệt trên các dòng mô hình khác (như GPT-4o, Claude 3.5 Sonnet hay DeepSeek).

## 10. Kết luận

> Tối đa 5 câu. Chỉ khẳng định điều số liệu hỗ trợ. Nêu một đề xuất cải tiến tiếp theo.

## Phụ lục

- Lệnh đã chạy (theo thứ tự):
- Thử thách mở rộng (nếu có): hướng chọn, kết quả, nhận xét.
- Ghi chú khác:
