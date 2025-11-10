# ✅ Checklist GitHub Secrets cho Python Image Generator

## 🔴 Bắt buộc (Required)

### Docker Hub
- [ ] **DOCKERHUB_USERNAME** - Username Docker Hub (ví dụ: `111299`)
- [ ] **DOCKERHUB_TOKEN** - Docker Hub Access Token hoặc password

### SSH Connection (cho Deploy)
- [ ] **SERVER_HOST** - Địa chỉ IP/domain của server (ví dụ: `157.66.100.63`)
- [ ] **SERVER_USER** - Username để SSH (ví dụ: `root`, `deploy`, `ubuntu`)
- [ ] **SSH_PRIVATE_KEY** - SSH private key (toàn bộ nội dung, bao gồm BEGIN và END lines)

## 🟡 Tùy chọn (Optional)

### Application Configuration
- [ ] **PEXELS_API_KEY** - API key cho Pexels (đã hardcode trong code, không bắt buộc)
- [ ] **API_KEY** - API key cho ứng dụng (đã hardcode trong code, không bắt buộc)

## 📝 Hướng dẫn từng bước

### Bước 1: Tạo Docker Hub Access Token

1. Đăng nhập vào [Docker Hub](https://hub.docker.com/)
2. Vào **Account Settings** → **Security** → **New Access Token**
3. Đặt tên token (ví dụ: `github-actions`)
4. Chọn quyền: **Read & Write** hoặc **Read, Write & Delete**
5. Copy token và lưu vào secret `DOCKERHUB_TOKEN`

**Lưu ý**: Token chỉ hiển thị một lần, hãy lưu lại ngay!

### Bước 2: Tạo SSH Key Pair

```bash
# Trên máy local
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_actions_imagegen

# Copy public key lên server
ssh-copy-id -i ~/.ssh/github_actions_imagegen.pub user@server

# Xem private key để copy vào GitHub Secrets
cat ~/.ssh/github_actions_imagegen
```

### Bước 3: Thêm Secrets vào GitHub

1. Vào repository → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Thêm từng secret theo checklist ở trên

## 🔐 Chi tiết từng Secret

### DOCKERHUB_USERNAME
```
111299
```
hoặc username Docker Hub của bạn

### DOCKERHUB_TOKEN
```
dckr_pat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
Docker Hub Access Token (bắt đầu với `dckr_pat_`)

**Cách tạo:**
1. Vào https://hub.docker.com/settings/security
2. Click **New Access Token**
3. Đặt tên và chọn quyền **Read & Write**
4. Copy token (chỉ hiển thị 1 lần)

### SERVER_HOST
```
157.66.100.63
```
hoặc
```
deploy.example.com
```

### SERVER_USER
```
root
```
hoặc
```
deploy
```

### SSH_PRIVATE_KEY
```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAFwAAAAdzc2gtcn
...
(nhiều dòng)
...
-----END OPENSSH PRIVATE KEY-----
```
**Lưu ý**: Copy toàn bộ key, bao gồm BEGIN và END lines!

### PEXELS_API_KEY (Optional)
```
EY2W2pV8aA0CN0sJOrPfKOl6osKlxnWnp9gdHo1HfwnaKuELZJHP7BNm
```
**Lưu ý**: Đã hardcode trong code, chỉ cần nếu muốn override

### API_KEY (Optional)
```
XzEcSl7aaW7wfeyxW74IGpGDBcM4noaO
```
**Lưu ý**: Đã hardcode trong code, chỉ cần nếu muốn override

## 📋 Tóm tắt Secrets cần thiết

### Tối thiểu (cho CI/CD hoạt động):
1. ✅ **DOCKERHUB_USERNAME** - Username Docker Hub
2. ✅ **DOCKERHUB_TOKEN** - Docker Hub Access Token
3. ✅ **SERVER_HOST** - IP/domain server
4. ✅ **SERVER_USER** - SSH username
5. ✅ **SSH_PRIVATE_KEY** - SSH private key

### Đầy đủ (nếu muốn override config):
6. ⚪ **PEXELS_API_KEY** - Pexels API key (optional)
7. ⚪ **API_KEY** - Application API key (optional)

## 🧪 Test sau khi cấu hình

1. Push code lên branch `main` hoặc `master`
2. Vào tab **Actions** trên GitHub
3. Xem workflow `CI/CD Python Image Generator Docker Deploy` chạy
4. Kiểm tra logs:
   - Build Docker image thành công
   - Push image lên Docker Hub
   - Test Docker image
   - Deploy lên server (nếu có)

## ⚠️ Lưu ý quan trọng

1. **DOCKERHUB_TOKEN**: Chỉ hiển thị một lần khi tạo, hãy lưu lại ngay
2. **SSH_PRIVATE_KEY**: Phải copy toàn bộ key, không được thiếu dòng BEGIN/END
3. **SERVER_USER**: Nên tạo user riêng cho deploy, không dùng root nếu có thể
4. **API_KEY & PEXELS_API_KEY**: Đã hardcode trong code, không bắt buộc thêm vào secrets
5. **Docker image name**: Sẽ là `{DOCKERHUB_USERNAME}/python-imagegen:latest`

## 🔍 Kiểm tra Secrets đã cấu hình

Vào repository → **Settings** → **Secrets and variables** → **Actions**

Bạn sẽ thấy danh sách secrets đã thêm. Đảm bảo có ít nhất 5 secrets bắt buộc ở trên.

## 📝 Ví dụ cấu hình đầy đủ

```
DOCKERHUB_USERNAME: 111299
DOCKERHUB_TOKEN: dckr_pat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SERVER_HOST: 157.66.100.63
SERVER_USER: root
SSH_PRIVATE_KEY: -----BEGIN OPENSSH PRIVATE KEY-----...
```

## 🚀 Sau khi cấu hình xong

1. Workflow sẽ tự động chạy khi push code lên `main`/`master`
2. Docker image sẽ được build và push lên Docker Hub
3. Image sẽ được deploy tự động lên server (nếu có cấu hình SSH)
4. Có thể pull image bằng: `docker pull 111299/python-imagegen:latest`

