"""Seed 20 sample rides with test users and orders."""
import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, sync_engine, Base
from app.models.user import User
from app.models.ride import Ride
from app.models.product import Product
from app.models.order import Order
from app.utils.security import get_password_hash

RIDES_DATA = [
    {
        "title": "ChatGPT Plus 家庭拼车，稳定半年老号",
        "product": "chatgpt-plus",
        "total_seats": 4,
        "price_per_month": 35,
        "duration": 6,
        "description": "美区老号，GPT-4o 无限使用，支持 DALL·E 和高级语音。已稳定运行半年，到期可续。每人独立子账号，互不影响。",
        "contact_info": "微信：gpt_plus_001",
        "contact_price": 5,
    },
    {
        "title": "Plus 拼车 3=1，最后一位",
        "product": "chatgpt-plus",
        "total_seats": 4,
        "price_per_month": 40,
        "duration": 3,
        "description": "已有 3 位车友，还差最后一位。月付 40 元，支持 GPT-4o、插件、联网搜索。随时可上车。",
        "contact_info": "微信：plus_last_seat",
        "contact_price": 3,
    },
    {
        "title": "ChatGPT Team 5人拼车，含管理后台",
        "product": "chatgpt-team",
        "total_seats": 5,
        "price_per_month": 55,
        "duration": 12,
        "description": "Team 版本含管理后台，更高 GPT-4o 限额，支持 DALL·E、高级数据分析。年付优惠，长期稳定。",
        "contact_info": "微信：team_5seats",
        "contact_price": 8,
    },
    {
        "title": "Team 企业级拼车，GPT-4o 无限畅享",
        "product": "chatgpt-team",
        "total_seats": 8,
        "price_per_month": 45,
        "duration": 6,
        "description": "企业级 Team 订阅，8 人拼车，每人独立空间。适合开发者和内容创作者，API 额度充足。",
        "contact_info": "Telegram：@team_gpt_biz",
        "contact_price": 6,
    },
    {
        "title": "ChatGPT Pro 拼车，o1 pro 无限用",
        "product": "chatgpt-pro",
        "total_seats": 3,
        "price_per_month": 280,
        "duration": 3,
        "description": "Pro 版本包含 o1 pro 模式，无限制 GPT-4o，最高优先级响应。适合重度用户和专业场景。",
        "contact_info": "微信：pro_unlimited",
        "contact_price": 15,
    },
    {
        "title": "Plus 学生拼车，性价比之选",
        "product": "chatgpt-plus",
        "total_seats": 4,
        "price_per_month": 30,
        "duration": 6,
        "description": "学生价拼车，月付仅 30 元。支持 GPT-4o 全部功能，适合写论文、编程、学习。已有 2 位同学。",
        "contact_info": "微信：student_gpt_30",
        "contact_price": 2,
    },
    {
        "title": "Team 技术团队拼车，API 额度充足",
        "product": "chatgpt-team",
        "total_seats": 6,
        "price_per_month": 50,
        "duration": 12,
        "description": "技术团队专用，API 调用额度高。支持代码解释器、知识库上传、自定义 GPT。年付更划算。",
        "contact_info": "邮箱：tech_team@gpt.com",
        "contact_price": 10,
    },
    {
        "title": "Plus 美区老号拼车，稳定可靠",
        "product": "chatgpt-plus",
        "total_seats": 4,
        "price_per_month": 38,
        "duration": 12,
        "description": "美区注册老号，已稳定运营 1 年以上。支持全部 Plus 功能，含插件商店和 GPTs。",
        "contact_info": "微信：us_plus_old",
        "contact_price": 5,
    },
    {
        "title": "Pro 拼车 2=1，高端用户专属",
        "product": "chatgpt-pro",
        "total_seats": 3,
        "price_per_month": 300,
        "duration": 6,
        "description": "已有 2 位高端用户，还差 1 位。Pro 全功能解锁，o1 pro 无限使用，优先级最高。",
        "contact_info": "Telegram：@pro_gpt_vip",
        "contact_price": 20,
    },
    {
        "title": "Plus 拼车季付，随时可退",
        "product": "chatgpt-plus",
        "total_seats": 4,
        "price_per_month": 42,
        "duration": 3,
        "description": "季付灵活，不满意随时退。GPT-4o 全功能，DALL·E 画图，高级语音对话。适合尝鲜用户。",
        "contact_info": "微信：flex_plus_q",
        "contact_price": 3,
    },
    {
        "title": "Team 设计师拼车，创意工作者首选",
        "product": "chatgpt-team",
        "total_seats": 5,
        "price_per_month": 48,
        "duration": 6,
        "description": "专为设计师和创意工作者打造，DALL·E 无限生成，支持图片上传分析。含知识库功能。",
        "contact_info": "微信：design_team_gpt",
        "contact_price": 6,
    },
    {
        "title": "Plus 年付超值拼车，月均仅 32 元",
        "product": "chatgpt-plus",
        "total_seats": 4,
        "price_per_month": 32,
        "duration": 12,
        "description": "年付优惠价，月均仅 32 元。长期稳定老号，支持全部 Plus 功能。到期自动续费提醒。",
        "contact_info": "微信：annual_plus_32",
        "contact_price": 4,
    },
    {
        "title": "Team 8人大车，人满即发",
        "product": "chatgpt-team",
        "total_seats": 8,
        "price_per_month": 40,
        "duration": 6,
        "description": "8 人大车，人满即发。Team 版本高限额，支持 GPT-4o、DALL·E、高级数据分析。性价比极高。",
        "contact_info": "微信：team_8big",
        "contact_price": 5,
    },
    {
        "title": "Plus 拼车，支持微信支付",
        "product": "chatgpt-plus",
        "total_seats": 4,
        "price_per_month": 36,
        "duration": 6,
        "description": "支持微信转账付款，安全便捷。GPT-4o 全功能，插件商店，GPTs 创建。已运营 3 个月。",
        "contact_info": "微信：wechat_pay_plus",
        "contact_price": 3,
    },
    {
        "title": "Pro 拼车独享位，尊贵体验",
        "product": "chatgpt-pro",
        "total_seats": 2,
        "price_per_month": 350,
        "duration": 3,
        "description": "仅 2 人拼车，接近独享体验。Pro 全功能，o1 pro 无限使用。适合对响应速度要求极高的用户。",
        "contact_info": "微信：pro_vip_2",
        "contact_price": 25,
    },
    {
        "title": "Plus 新手友好拼车，附教程",
        "product": "chatgpt-plus",
        "total_seats": 4,
        "price_per_month": 35,
        "duration": 3,
        "description": "新手友好，附赠 ChatGPT 使用教程和提示词大全。支持 GPT-4o 全功能，有问题随时问。",
        "contact_info": "微信：newbie_friendly",
        "contact_price": 2,
    },
    {
        "title": "Team 程序员拼车，GitHub Copilot 联动",
        "product": "chatgpt-team",
        "total_seats": 6,
        "price_per_month": 52,
        "duration": 12,
        "description": "程序员专属拼车，Team 版本高限额。支持代码解释器、终端执行、项目分析。适合全栈开发。",
        "contact_info": "Telegram：@coder_team_gpt",
        "contact_price": 8,
    },
    {
        "title": "Plus 拼车 2=2，双人同行优惠",
        "product": "chatgpt-plus",
        "total_seats": 4,
        "price_per_month": 34,
        "duration": 6,
        "description": "已有 2 位车友，还差 2 位。双人同行价，月付 34 元。GPT-4o 全功能，稳定可靠。",
        "contact_info": "微信：pair_plus_34",
        "contact_price": 3,
    },
    {
        "title": "Team 跨国团队拼车，多语言支持",
        "product": "chatgpt-team",
        "total_seats": 10,
        "price_per_month": 38,
        "duration": 12,
        "description": "10 人大车，适合跨国团队。支持中英日韩等多语言，翻译质量极高。年付月均仅 38 元。",
        "contact_info": "邮箱：global_team@chat.com",
        "contact_price": 5,
    },
    {
        "title": "Plus 拼车限时特惠，先到先得",
        "product": "chatgpt-plus",
        "total_seats": 4,
        "price_per_month": 28,
        "duration": 3,
        "description": "限时特惠价，月付仅 28 元！GPT-4o 全功能，支持 DALL·E 和高级语音。名额有限，先到先得。",
        "contact_info": "微信：flash_sale_plus",
        "contact_price": 1,
    },
]


def seed_rides():
    db = SessionLocal()
    try:
        # Check if rides already seeded
        existing_count = db.query(Ride).count()
        if existing_count >= 20:
            print(f"Rides table already has {existing_count} rides. Skipping seed.")
            return

        # Create test users as ride owners
        owners = []
        for i in range(1, 11):
            email = f"owner{i}@busgpt.local"
            phone = f"1380000{i:04d}"
            user = db.query(User).filter(User.email == email).first()
            if not user:
                user = User(
                    email=email,
                    phone=phone,
                    nickname=f"车友{i}号",
                    avatar=f"https://api.dicebear.com/7.x/avataaars/svg?seed=owner{i}",
                    role="user",
                    password_hash=get_password_hash("123456"),
                    email_verified_at=datetime.utcnow(),
                )
                db.add(user)
                db.flush()
            owners.append(user)

        # Create rides
        now = datetime.utcnow()
        for idx, data in enumerate(RIDES_DATA):
            owner = owners[idx % len(owners)]
            created = now - timedelta(days=30 - idx)
            warranty_days = 365 if data["duration"] >= 12 else data["duration"] * 30
            expires = created + timedelta(days=warranty_days)
            ride = Ride(
                title=data["title"],
                product=data["product"],
                owner_id=owner.id,
                total_seats=data["total_seats"],
                recruit_seats=max(data["total_seats"] - 1, 1),
                price_per_month=data["price_per_month"],
                duration=data["duration"],
                warranty_days=warranty_days,
                description=data["description"],
                contact_info=data["contact_info"],
                contact_price=data["contact_price"],
                status="open",
                created_at=created,
                expires_at=expires,
            )
            db.add(ride)

        db.flush()

        # Create some test orders (purchases) for a buyer user
        buyer_email = "buyer@busgpt.local"
        buyer_phone = "13900000001"
        buyer = db.query(User).filter(User.email == buyer_email).first()
        if not buyer:
            buyer = User(
                email=buyer_email,
                phone=buyer_phone,
                nickname="测试买家",
                avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=buyer",
                role="user",
                password_hash=get_password_hash("123456"),
                email_verified_at=datetime.utcnow(),
            )
            db.add(buyer)
            db.flush()

        # Buyer purchases first 5 rides
        all_rides = db.query(Ride).order_by(Ride.id).all()
        for ride in all_rides[:5]:
            order = Order(
                user_id=buyer.id,
                ride_id=ride.id,
                amount=ride.contact_price,
                status="paid",
                payment_provider="mock",
                payment_status="paid",
                paid_at=now,
            )
            db.add(order)

        db.commit()
        print(f"Successfully seeded {len(RIDES_DATA)} rides, {len(owners)} owners, 1 buyer, 5 orders.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding rides: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_rides()
