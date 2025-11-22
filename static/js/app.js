// تطبيق إدارة الوسائط الاجتماعية - الإصدار 2.0
class SocialMediaManager {
    constructor() {
        this.apiBase = '/api';
        this.currentUser = null;
        this.sessionId = localStorage.getItem('sessionId');
        this.init();
    }

    init() {
        this.checkSystemStatus();
        this.loadCurrentUser();
        this.setupEventListeners();
        
        // إذا كان هناك جلسة نشطة، تحميل البيانات تلقائياً
        if (this.sessionId) {
            this.loadUserData();
        }
    }

    setupEventListeners() {
        // تحديث تلقائي للحسابات كل 30 ثانية
        setInterval(() => {
            if (this.sessionId) {
                this.loadSocialAccounts();
            }
        }, 30000);
    }

    async checkSystemStatus() {
        try {
            const response = await fetch(`${this.apiBase}/health`);
            const data = await response.json();
            
            const statusElement = document.getElementById('systemStatus');
            if (data.status === 'صحي') {
                statusElement.innerHTML = '✅ النظام يعمل بشكل طبيعي';
                statusElement.style.background = 'rgba(40, 167, 69, 0.2)';
            } else {
                statusElement.innerHTML = '⚠️ هناك مشكلة في النظام';
                statusElement.style.background = 'rgba(255, 193, 7, 0.2)';
            }
        } catch (error) {
            console.error('خطأ في فحص حالة النظام:', error);
            document.getElementById('systemStatus').innerHTML = '❌ تعذر الاتصال بالنظام';
        }
    }

    async apiCall(endpoint, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            }
        };

        // إضافة token المصادقة إذا كان موجوداً
        if (this.sessionId) {
            defaultOptions.headers['Authorization'] = `Bearer ${this.sessionId}`;
        }

        const finalOptions = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(`${this.apiBase}${endpoint}`, finalOptions);
            const data = await response.json();
            
            return {
                success: response.ok,
                data: data,
                status: response.status
            };
        } catch (error) {
            return {
                success: false,
                error: 'تعذر الاتصال بالخادم',
                status: 0
            };
        }
    }

    // إدارة المستخدمين
    async register() {
        const username = document.getElementById('regUsername').value;
        const email = document.getElementById('regEmail').value;
        const password = document.getElementById('regPassword').value;

        if (!username || !email || !password) {
            this.showMessage('registerMessage', 'جميع الحقول مطلوبة', 'error');
            return;
        }

        if (password.length < 6) {
            this.showMessage('registerMessage', 'كلمة المرور يجب أن تكون 6 أحرف على الأقل', 'error');
            return;
        }

        const result = await this.apiCall('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ username, email, password })
        });

        if (result.success) {
            this.sessionId = result.data.session_id;
            this.currentUser = result.data.user;
            localStorage.setItem('sessionId', this.sessionId);
            this.showMessage('registerMessage', result.data.message, 'success');
            this.switchTab('profile');
            this.loadUserData();
        } else {
            this.showMessage('registerMessage', result.data.error, 'error');
        }
    }

    async login() {
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        if (!email || !password) {
            this.showMessage('loginMessage', 'البريد الإلكتروني وكلمة المرور مطلوبان', 'error');
            return;
        }

        const result = await this.apiCall('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });

        if (result.success) {
            this.sessionId = result.data.session_id;
            this.currentUser = result.data.user;
            localStorage.setItem('sessionId', this.sessionId);
            this.showMessage('loginMessage', result.data.message, 'success');
            this.switchTab('profile');
            this.loadUserData();
        } else {
            this.showMessage('loginMessage', result.data.error, 'error');
        }
    }

    async getProfile() {
        const result = await this.apiCall('/auth/profile');
        
        if (result.success) {
            this.currentUser = result.data.user;
            this.displayUserProfile(result.data.user);
        } else {
            this.showMessage('profileInfo', result.data.error, 'error');
            this.logout();
        }
    }

    // الحسابات الاجتماعية
    async connectSocialAccount() {
        const platform = document.getElementById('socialPlatform').value;
        const username = document.getElementById('socialUsername').value;
        const accessToken = document.getElementById('socialToken').value;

        if (!platform || !username || !accessToken) {
            this.showMessage('accountsList', 'جميع الحقول مطلوبة', 'error');
            return;
        }

        const result = await this.apiCall('/social/connect', {
            method: 'POST',
            body: JSON.stringify({ platform, username, access_token: accessToken })
        });

        if (result.success) {
            this.showMessage('accountsList', result.data.message, 'success');
            this.loadSocialAccounts();
            // مسح الحقول
            document.getElementById('socialUsername').value = '';
            document.getElementById('socialToken').value = '';
        } else {
            this.showMessage('accountsList', result.data.error, 'error');
        }
    }

    async loadSocialAccounts() {
        const result = await this.apiCall('/social/accounts');
        
        if (result.success) {
            this.displaySocialAccounts(result.data.accounts);
        } else {
            this.showMessage('accountsList', 'تعذر تحميل الحسابات', 'error');
        }
    }

    // عرض البيانات
    displayUserProfile(user) {
        const profileElement = document.getElementById('profileInfo');
        profileElement.innerHTML = `
            <div class="profile-header">
                <h3>معلومات المستخدم</h3>
            </div>
            <div class="profile-details">
                <p><strong>اسم المستخدم:</strong> ${user.username}</p>
                <p><strong>البريد الإلكتروني:</strong> ${user.email}</p>
                <p><strong>تاريخ الإنشاء:</strong> ${new Date(user.created_at).toLocaleDateString('ar-SA')}</p>
                <p><strong>عدد الحسابات الاجتماعية:</strong> ${user.social_accounts_count}</p>
                <p><strong>اللغة:</strong> ${user.preferences.language === 'ar' ? 'العربية' : user.preferences.language}</p>
                <p><strong>المنطقة الزمنية:</strong> ${user.preferences.timezone}</p>
            </div>
            <button class="btn btn-secondary" onclick="app.logout()">تسجيل الخروج</button>
        `;
        profileElement.classList.add('active');
    }

    displaySocialAccounts(accounts) {
        const accountsElement = document.getElementById('accountsList');
        
        if (accounts.length === 0) {
            accountsElement.innerHTML = '<p class="no-accounts">لا توجد حسابات مربوطة بعد</p>';
            return;
        }

        accountsElement.innerHTML = accounts.map(account => `
            <div class="account-card">
                <div class="account-icon">
                    ${this.getPlatformIcon(account.platform)}
                </div>
                <div class="account-info">
                    <div class="account-platform">${this.getPlatformName(account.platform)}</div>
                    <div class="account-username">@${account.username}</div>
                    <div class="account-stats">
                        <small>متابعون: ${account.stats.followers} | منشورات: ${account.stats.posts}</small>
                    </div>
                </div>
                <div class="account-status ${account.is_active ? 'active' : 'inactive'}">
                    ${account.is_active ? 'نشط' : 'غير نشط'}
                </div>
            </div>
        `).join('');
    }

    getPlatformIcon(platform) {
        const icons = {
            twitter: '🐦',
            facebook: '📘',
            instagram: '📷',
            linkedin: '💼'
        };
        return icons[platform] || '🔗';
    }

    getPlatformName(platform) {
        const names = {
            twitter: 'تويتر (X)',
            facebook: 'فيسبوك',
            instagram: 'إنستغرام',
            linkedin: 'لينكدإن'
        };
        return names[platform] || platform;
    }

    // أدوات مساعدة
    showMessage(elementId, message, type) {
        const element = document.getElementById(elementId);
        element.textContent = message;
        element.className = `message ${type}`;
        element.style.display = 'block';

        // إخفاء الرسالة بعد 5 ثواني
        setTimeout(() => {
            element.style.display = 'none';
        }, 5000);
    }

    switchTab(tabName) {
        // إخفاء جميع المحتويات
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        
        // إلغاء تنشيط جميع الألسنة
        document.querySelectorAll('.tab').forEach(tab => {
            tab.classList.remove('active');
        });
        
        // إظهار المحتوى المطلوب
        document.getElementById(tabName).classList.add('active');
        
        // تنشيط اللسان المطلوب
        document.querySelector(`.tab[onclick="switchTab('${tabName}')"]`).classList.add('active');

        // تحميل البيانات إذا لزم الأمر
        if (tabName === 'profile' && this.sessionId) {
            this.getProfile();
        } else if (tabName === 'social' && this.sessionId) {
            this.loadSocialAccounts();
        }
    }

    loadCurrentUser() {
        if (this.sessionId) {
            this.getProfile();
        }
    }

    loadUserData() {
        this.getProfile();
        this.loadSocialAccounts();
    }

    logout() {
        this.sessionId = null;
        this.currentUser = null;
        localStorage.removeItem('sessionId');
        
        // إعادة تعيين الواجهة
        document.getElementById('profileInfo').innerHTML = '';
        document.getElementById('profileInfo').classList.remove('active');
        document.getElementById('accountsList').innerHTML = '';
        
        this.switchTab('login');
        this.showMessage('loginMessage', 'تم تسجيل الخروج بنجاح', 'success');
    }
}

// تهيئة التطبيق
const app = new SocialMediaManager();

// الدوال العامة للاستدعاء من HTML
function switchTab(tabName) {
    app.switchTab(tabName);
}

function register() {
    app.register();
}

function login() {
    app.login();
}

function getProfile() {
    app.getProfile();
}

function connectSocialAccount() {
    app.connectSocialAccount();
}

function loadSocialAccounts() {
    app.loadSocialAccounts();
}

// إضافة إدخال عند الضغط على Enter
document.addEventListener('DOMContentLoaded', function() {
    // التسجيل
    document.getElementById('regPassword').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') register();
    });

    // تسجيل الدخول
    document.getElementById('loginPassword').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') login();
    });

    // ربط الحسابات الاجتماعية
    document.getElementById('socialToken').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') connectSocialAccount();
    });
});
