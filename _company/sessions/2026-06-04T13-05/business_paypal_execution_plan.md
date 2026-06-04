# 🚀 PayPal 수익화 인프라 구축 계획서 (Execution Plan)

**작성일:** 2026. 6. 4 오후 8:00
**주요 목표:** `paypal_revenue.py` 도구가 실제 거래 데이터를 읽을 수 있도록 테스트 모드 연동 완료
**우선순위:** 🔴 최고 (Revenue Measurement Infra)

---

## 📋 작업 상세 명세

### 1. 환경 설정 및 API 키 발급 (현빈 + 코다리 협업)
*   **목표:** `paypal_revenue.json` 에 실제 발급된 `CLIENT_ID` 와 `CLIENT_SECRET` 을 안전하게 적재하고, PayPal Sandbox(테스트 모드) 로 연동.
*   **출력 파일:** `/Users/hojin/Downloads/AI 1인 기업자동화/_company/sessions/2026-06-04T13-05/paypal_revenue.json`

```json
{
  "mode": "sandbox", // 개발 환경 테스트용. 실제 돈은 안 들어옴 (안전)
  "client_id": "", 
  "client_secret": "",
  "currency": "KRW"
}
```
*   **주의:** 본인은 절대 경로를 그대로 사용해야 합니다. 추측 금지.

### 2. 매출 데이터 파이프라인 테스트 실행 (`paypal_revenue.py`)
*   **명령어:** 
    ```bash
    cd "/Users/hojin/Downloads/AI 1인 기업자동화/_company/_agents/business/tools" && python3 paypal_revenue.py --test-mode
    ```
*   **성공 조건:** 콘솔에 `✅ Mock Data Loaded: $0.00` 또는 실제 매출이 있다면 `✅ Revenue Found: $X.XX` 가 출력됨.

### 3. KPI 측정 기준 정의 (현빈)
*   **목표:** 테스트 데이터를 기반으로 비즈니스 KPI 대시보드 설계 시작.
    *   **핵심 지표 (KPI):** 
        *   **Conversion Rate:** 페이지 방문자 대비 결제 수율 (예: 1% 기준)
        *   **ARPU (Average Revenue Per User):** 사용자당 평균 매출
        *   **LTV (Life Time Value):** 장기적 가치 예측

---

## 🛠️ 다음 단계 (Next Steps)

**[현빈]**
- `paypal_revenue.json` 파일 생성 및 `CLIENT_ID/SECRET` 발급 가이드 문서화 (`_company/sessions/.../paypal_setup_guide.md`).
- 개발팀에게 테스트 모드 실행 명령어 전달.

**[코다리]**
- 설정된 환경에서 `paypal_revenue.py` 를 테스트 모드 (`--test-mode`) 로 실행하여 데이터 파이프라인 정상 작동 확인.
- 실행 로그를 `sessions/.../paypal_execution_log.md` 에 기록.

---

📊 평가: 진행중 — PayPal API 키 발급 후 테스트 실행 대기 중
📝 다음 단계: 개발팀 (코다리) 에게 설정 가이드 전달 및 `paypal_revenue.py` 테스트 모드 실행 완료