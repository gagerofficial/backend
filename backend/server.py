from fastapi import FastAPI, APIRouter, Body
from starlette.middleware.cors import CORSMiddleware
import os
import uvicorn
import logging
from pydantic import BaseModel, Field
from typing import List, Optional, Set
import uuid
from datetime import datetime
import requests

# Create the main app without a prefix
app = FastAPI()

registered_tokens: Set[str] = set()

class TokenSchema(BaseModel):
    token: str

api_router = APIRouter(prefix="/api")

@api_router.post("/register-token")
async def register_token(data: TokenSchema):
    registered_tokens.add(data.token)
    print(f"DEBUG: Új token regisztrálva: {data.token}")
    return {"status": "ok", "message": "Token mentve"}

def send_push_to_all(title: str, body: str):
    url = "https://exp.host/--/api/v2/push/send"
    payloads = []
    for token in registered_tokens:
        payloads.append({
            "to": token,
            "title": title,
            "body": body,
            "sound": "default"
        })
    if payloads:
        response = requests.post(url, json=payloads)
        return response.json()
    return {"message": "Nincs regisztrált eszköz."}

@api_router.post("/send-test-push")
async def test_push():
    return send_push_to_all("PatakyApp Teszt", "Működik az értesítés! 🚀")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ez engedélyezi, hogy bármilyen címről (pl. localhost-ról is) elérjék
    allow_credentials=True,
    allow_methods=["*"],  # Engedélyezi a GET, POST stb. kéréseket
    allow_headers=["*"],  # Engedélyezi az összes fejlécet
)

# Create a router with the /api prefix


# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class NewsArticle(BaseModel):
    id: str
    title: str
    subtitle: str
    content: str
    image_url: Optional[str] = None
    date: str
    category: str

class Course(BaseModel):
    id: str
    title: str
    description: str
    duration: str
    type: str  # "nappali", "esti", "felnott"
    icon: str

class StaffMember(BaseModel):
    id: str
    name: str
    position: str
    department: str
    email: Optional[str] = None

class Event(BaseModel):
    id: str
    title: str
    date: str
    description: str
    location: str

class ContactInfo(BaseModel):
    phone: str
    fax: str
    email: str
    address: str
    postal_address: str
    om_code: str
    social_links: dict

# Static data for the school
SCHOOL_INFO = {
    "name": "BMSZC Pataky István Híradásipari és Informatikai Technikum",
    "short_name": "Pataky Technikum",
    "description": "A Budapesti Műszaki Szakképzési Centrum Pataky István Híradásipari és Informatikai Technikum nappali és esti szakképzést kínál.",
    "founded": "1952",
    "motto": "A jövőt nálunk tanulod!"
}

CONTACT_INFO = ContactInfo(
    phone="+36 70 502 1012",
    fax="+36 1 265 1664",
    email="pataky@pataky.hu",
    address="1101 Budapest, Salgótarjáni út 53./b",
    postal_address="1101 Budapest, Salgótarjáni út 53./b",
    om_code="203058/008",
    social_links={
        "facebook": "https://hu-hu.facebook.com/patakyszki/",
        "instagram": "https://www.instagram.com/patakytechnikum/",
        "linkedin": "https://www.linkedin.com/school/37770007/"
    }
)

NEWS_ARTICLES = [
    NewsArticle(
        id="1",
        title="Felvételi információk",
        subtitle="Központi írásbeli felvételi információk",
        content="Folyamatosan frissített információk a középiskolai felvételi folyamattal kapcsolatban. Az írásbeli vizsgák időpontjai és helyszínei elérhetőek az iskola honlapján. Kérjük, kövesse figyelemmel az aktuális információkat!",
        image_url=None,
        date="2025-01-15",
        category="Felvételi"
    ),
    NewsArticle(
        id="2",
        title="Felnőttoktatás – Új szakma, új lehetőség!",
        subtitle="Indul a Felnőttképzési jelentkezés",
        content="Ismerd meg, milyen szakmákkal várunk! A felnőttoktatás keretében lehetőség van új szakma megszerzésére, rugalmas időbeosztással. Jelentkezz most és kezdj új karriert!",
        image_url=None,
        date="2025-01-28",
        category="Felnőttoktatás"
    ),
    NewsArticle(
        id="3",
        title="A jövőt nálunk tanulod!",
        subtitle="Mitől vagyunk jobbak és többek?",
        content="Beiskolázás 2026-2027. Modern technológiák, tapasztalt oktatók, ipari partnerkapcsolatok. Válaszd a Pataky Technikumot és építsd jövődet velünk!",
        image_url=None,
        date="2025-01-06",
        category="Beiskolázás"
    ),
    NewsArticle(
        id="4",
        title="Történelmi tanulmányi út",
        subtitle="4 napos római városnézés diákoknak",
        content="2026.03.17-20 között szervezett római tanulmányi út. Jelentkezés az osztályfőnököknél. Korlátozott létszám, ne maradj le!",
        image_url=None,
        date="2025-02-05",
        category="Események"
    ),
    NewsArticle(
        id="5",
        title="Fizika emelt szintű érettségi kísérletek",
        subtitle="Felkészítő anyagok elérhetőek",
        content="Az emelt szintű fizika érettségire készülők számára elérhetővé tettük a kísérleti videókat és leírásokat. A tananyag folyamatosan bővül.",
        image_url=None,
        date="2025-01-20",
        category="Tanulás"
    )
]

COURSES = [
    Course(
        id="1",
        title="Szoftverfejlesztő és -tesztelő",
        description="Modern programozási nyelvek, webes és mobil alkalmazásfejlesztés, szoftvertesztelési módszerek.",
        duration="5 év (technikum)",
        type="technikum",
        icon="code"
    ),
    Course(
        id="2",
        title="Hálózati informatikus",
        description="Számítógépes hálózatok tervezése, telepítése és üzemeltetése. Cisco és Microsoft képzések.",
        duration="5 év (technikum)",
        type="technikum",
        icon="wifi"
    ),
    Course(
        id="3",
        title="Infokommunikációs hálózatépítő és -üzemeltető",
        description="Távközlési és informatikai hálózatok építése, karbantartása.",
        duration="3 év (szakképző)",
        type="szakkepzo",
        icon="network-check"
    ),
    Course(
        id="4",
        title="Elektronikai technikus",
        description="Elektronikai eszközök tervezése, fejlesztése és javítása.",
        duration="5 év (technikum)",
        type="technikum",
        icon="hardware-chip"
    ),
    Course(
        id="5",
        title="Felnőtt szakképzés - IT",
        description="Felnőttek számára esti tagozaton elérhető informatikai képzések.",
        duration="2-3 év (esti)",
        type="felnott",
        icon="school"
    ),
    Course(
        id="6",
        title="Elektrotechnikai technikus",
        description="Elektromos rendszerek tervezése és kivitelezése.",
        duration="5 év (technikum)",
        type="technikum",
        icon="flash"
    )
]

STAFF_MEMBERS = [
    StaffMember(id="1", name="Tóth Imre", position="igazgató", department="Vezetőség", email="imre@pataky.hu"),
    StaffMember(id="2", name="Székelyné Polgár Klára", position="igazgatóhelyettes", department="Vezetőség", email="pklara@pataky.hu"),
    StaffMember(id="3", name="Harangozó Attila", position="igazgatóhelyettes", department="Vezetőség", email="gyak@pataky.hu"),
    StaffMember(id="4", name="Végh Orsolya", position="igazgatóhelyettes", department="Vezetőség", email="vegh.orsolya@pataky.hu"),
    StaffMember(id="5", name="Titkárság", position="Adminisztráció", department="Iroda", email="pataky@pataky.hu"),
]

# Teachers data
class Teacher(BaseModel):
    id: str
    name: str
    subject: str
    department: str
    email: Optional[str] = None
    phone: Optional[str] = None
    office: Optional[str] = None
    consultation_hours: Optional[str] = None

TEACHERS = [
    Teacher(id="T1", name="Czene István", subject="magyar nyelv és irodalom – történelem – állampolgári ismeretek", department="Közismeret", email="istvanczene@gmail.com", office="11.B"),
    Teacher(id="T2", name="Harsányi Tünde", subject="magyar nyelv és irodalom – történelem – állampolgári ismeretek", department="Közismeret", email="harsanyit@pataky.hu", office="11.D"),
    Teacher(id="T3", name="Haller Zoltán", subject="magyar nyelv és irodalom – történelem", department="Közismeret", email="haller.zoltan@pataky.hu", office="11.E"),
    Teacher(id="T4", name="Szalai József", subject="magyar nyelv és irodalom", department="Közismeret", email="szalai.jozsef@pataky.hu", office="9.B"),
    Teacher(id="T5", name="Tózsa Éva", subject="magyar nyelv és irodalom", department="Közismeret", email="tozsa.eva77@gmail.com", office="11.A"),
    Teacher(id="T6", name="Csabay Károly", subject="Matematika", department="Közismeret", email="csabay.karoly@pataky.hu"),
    Teacher(id="T7", name="Hegedűs László", subject="matematika", department="Közismeret", email="hegedus.laszlo@pataky.hu", office="12.C"),
    Teacher(id="T8", name="Katona Csaba", subject="Fizika", department="Közismeret", email="kacsa@pataky.hu", office="12.C"),
    Teacher(id="T9", name="Novotny László", subject="matematika", department="Közismeret", email="novotny.laszlo@pataky.hu"),
    Teacher(id="T10", name="Szabó Márta", subject="matematika, digitális kultúra", department="Közismeret", email="szabo.marta@pataky.hu"),
    Teacher(id="T11", name="Fekete Tamás", subject="IKT projektmunka, Programozás, Informatikai alapok", department="Informatika", email="fekete.tamas@pataky.hu"),
    Teacher(id="T12", name="Gersei Gábor", subject="Hálózatok gyakorlat, Informatikai alapok", department="Informatika", email="gersei@pataky.hu"),
    Teacher(id="T13", name="Gödöny Péter", subject="Informatikai alapok, Programozás, Digitális kultúra", department="Informatika", email="godony.peter@pataky.hu", office="12.D"),
    Teacher(id="T14", name="Gudmon Zsolt", subject="Hálózatszerelés, Távközlés elektronika, Optikai hálózatok", department="Informatika", email="gudmon.zsolt@pataky.hu", office="13.A és 13.B"),
    Teacher(id="T15", name="Hódi Gyula", subject="Programozási alapok, IKT projektmunka I., Digitális kultúra", department="Informatika", email="hodi.gyula@pataky.hu"),
    Teacher(id="T16", name="Matuszczak Róbert", subject="IKT projektmunka, Digitális kultúra, Szerver szolgáltatások", department="Informatika", email="rob@pataky.hu", office="9.C és 13.C"),
    Teacher(id="T17", name="Virágh Krisztián", subject="Szerverek és felhőszolgáltatások, IP hálózatok", department="Informatika", email="viragh.krisztian@pataky.hu", office="10.B"),
    Teacher(id="T18", name="Pesti Zoltán", subject="Hálózatok I és II, Felhőszolgáltatások", department="Informatika", email="pezo@pataky.hu", office="13.D"),
    Teacher(id="T19", name="Apáti János", subject="Programozási alapok, Informatikai és távközlési alapok", department="Informatika", email="apati.janos@pataky.hu", office="11.C"),
    Teacher(id="T20", name="Abrók István", subject="távközlés, IKT projektmunka II.", department="Informatika", email="abrok.istvan@pataky.hu"),
    Teacher(id="T21", name="Kovács Annabella", subject="digitális kultúra", department="Informatika", email="bella@pataky.hu"),
    Teacher(id="T22", name="Kőhalmi Ábel", subject="IP hálózatok", department="Informatika", email="kohalmi.abel@pataky.hu"),
    Teacher(id="T23", name="Szabó Viktória Anikó", subject="digitális kultúra, pénzügyi és vállalkozói ismeretek", department="Informatika", email="szabo.viktoria@pataky.hu"),
    Teacher(id="T24", name="Bruder György", subject="informatika", department="Informatika", email="bruder.gyorgy@pataky.hu"),
    Teacher(id="T25", name="Visi Gergő Bálint", subject="IKT Projektmunka, Távközlés", department="Informatika", email="visi.gergo@pataky.hu"),
    Teacher(id="T26", name="Gáll Katalin Márta", subject="Angol nyelv", department="Közismeret", email="gall.katalin@pataky.hu", office="12.B"),
    Teacher(id="T27", name="Tóth-Káli Dominika", subject="angol nyelv", department="Közismeret", email="kali.dominika@pataky.hu"),
    Teacher(id="T28", name="Kántor Sándor", subject="Angol nyelv", department="Közismeret", email="kantor.sandor@pataky.hu"),
    Teacher(id="T29", name="Szerencsi Andrea", subject="Angol nyelv", department="Közismeret", email="szerencsi.andrea@pataky.hu", office="10.C"),
    Teacher(id="T30", name="Kemény Orsolya", subject="Angol nyelv", department="Közismeret", email="kemenyorsolya@pataky.hu"),
    Teacher(id="T31", name="Szauterné Pödrőczi Éva", subject="angol nyelv", department="Közismeret", email="szauter.eva@pataky.hu"),
    Teacher(id="T32", name="Ferencz Noémi", subject="Angol nyelv", department="Közismeret", email="ferencz.noemi@pataky.hu"),
    Teacher(id="T33", name="Törteli Tibor", subject="testnevelés", department="Közismeret", email="torteli.tibor@pataky.hu", office="10.A"),
    Teacher(id="T34", name="Gazsó Réka", subject="testnevelés", department="Közismeret", email="gazso.reka@pataky.hu"),
    Teacher(id="T35", name="Rozmán Balázs", subject="testnevelés", department="Közismeret", email="rozman.balazs@pataky.hu", office="9.A"),
]

# Menu data
class MenuItem(BaseModel):
    name: str
    allergens: Optional[List[str]] = None

class DailyMenu(BaseModel):
    day: str
    date: str
    soup: MenuItem
    main_course: MenuItem
    dessert: Optional[MenuItem] = None

WEEKLY_MENU = [
    DailyMenu(
        day="Hétfő",
        date="2025-02-16",
        soup=MenuItem(name="Legényfogóleves", allergens=["glutén", "tojás"]),
        main_course=MenuItem(name="Morzsás nudli porcukorral", allergens=["glutén", "tojás", "tej"]),
        dessert=MenuItem(name="Gyümölcs")
    ),
    DailyMenu(
        day="Kedd",
        date="2025-02-17",
        soup=MenuItem(name="Csonleves cérnametélttel", allergens=["glutén", "tojás"]),
        main_course=MenuItem(name="Erdélyi rakott káposzta", allergens=[]),
        dessert=MenuItem(name="-")
    ),
    DailyMenu(
        day="Szerda",
        date="2025-02-18",
        soup=MenuItem(name="Zöldséges karfiolleves", allergens=[]),
        main_course=MenuItem(name="Burgonya főzelék, sertés pörkölt", allergens=["glutén"]),
        dessert=MenuItem(name="-")
    ),
    DailyMenu(
        day="Csütörtök",
        date="2025-02-19",
        soup=MenuItem(name="Bazsalikomos paradicsomleves"),
        main_course=MenuItem(name="Provence-i csirkecomb, rizi-bizi"),
        dessert=MenuItem(name="-")
    ),
    DailyMenu(
        day="Péntek",
        date="2025-02-20",
        soup=MenuItem(name="Francia hagymaleves, sajtos cruton", allergens=["glutén", "tej"]),
        main_course=MenuItem(name="Vegán chilis bab"),
        dessert=MenuItem(name="Túró Rudi", allergens=["tej"])
    ),
]

# Gallery data
class GalleryImage(BaseModel):
    id: str
    url: str
    thumbnail: str
    caption: str

class GalleryAlbum(BaseModel):
    id: str
    title: str
    description: str
    date: str
    cover_image: str
    image_count: int
    images: List[GalleryImage]

GALLERY_ALBUMS = [
    GalleryAlbum(
        id="1",
        title="Szalagavató",
        description="Szalagavató 2026!",
        date="2026-01-16",
        cover_image="https://scontent-vie1-1.xx.fbcdn.net/v/t39.30808-6/615999093_1484899656973052_3679359874566733709_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=f727a1&_nc_ohc=-_VscXN787kQ7kNvwF6b7tu&_nc_oc=Adn5X37ON70AYpjwrO-Q-Z4VsXXlIWohlUd0wmpEFZV38kNHqSm-X2g9PszIAcALV0vgt3LVQfv0QbsUEcAegfV_&_nc_zt=23&_nc_ht=scontent-vie1-1.xx&_nc_gid=0iy02J978rdqJrz1kYCG1Q&oh=00_AfvEC9a0nRubqZQ78kRLgXBXjHv6OYHTvknoGZsf-C90uQ&oe=69958FD3",
        image_count=4,
        images=[
            GalleryImage(id="1-1", url="https://scontent-vie1-1.xx.fbcdn.net/v/t39.30808-6/617054003_1484900333639651_3236773686781858520_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=f727a1&_nc_ohc=h5TSknhDbg8Q7kNvwEze7vW&_nc_oc=AdnGtU-K8O21p_aWzkJdweVdzq9uv6NjQd4cHJeqKR7ZkAkSsZJF4T-YalacC3X2BLGbY1UrBT6YnGoOCWKnzWRV&_nc_zt=23&_nc_ht=scontent-vie1-1.xx&_nc_gid=0VDouI3uibjrL1pMm_WivQ&oh=00_AftmikQ7DdLgyyHA1N9gB5Ii-qV7d2Gu38fTL0rMEwbQDw&oe=69956FE0", thumbnail="https://scontent-vie1-1.xx.fbcdn.net/v/t39.30808-6/617054003_1484900333639651_3236773686781858520_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=f727a1&_nc_ohc=h5TSknhDbg8Q7kNvwEze7vW&_nc_oc=AdnGtU-K8O21p_aWzkJdweVdzq9uv6NjQd4cHJeqKR7ZkAkSsZJF4T-YalacC3X2BLGbY1UrBT6YnGoOCWKnzWRV&_nc_zt=23&_nc_ht=scontent-vie1-1.xx&_nc_gid=0VDouI3uibjrL1pMm_WivQ&oh=00_AftmikQ7DdLgyyHA1N9gB5Ii-qV7d2Gu38fTL0rMEwbQDw&oe=69956FE0", caption="Éremátadás"),
            GalleryImage(id="1-2", url="https://scontent-vie1-1.xx.fbcdn.net/v/t39.30808-6/615928702_1484900066973011_5904557219256711769_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=f727a1&_nc_ohc=NqcAGs7s1O4Q7kNvwGTsMHV&_nc_oc=AdlMixLOIwNRZkIKeKtFmkhREBg6uEld68D6UeU8ZOLfnopt1KrCGCUSYDT5ikSMJy1C6IZku8TXMnzmYNhw2odH&_nc_zt=23&_nc_ht=scontent-vie1-1.xx&_nc_gid=d6WedswgV-xbWMhBdBPvvA&oh=00_Afuj3uT1eWt5Vf_h-xylGsqjPhMGitgVhbtjr9dR07dMVA&oe=69956211", thumbnail="https://scontent-vie1-1.xx.fbcdn.net/v/t39.30808-6/615928702_1484900066973011_5904557219256711769_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=f727a1&_nc_ohc=NqcAGs7s1O4Q7kNvwGTsMHV&_nc_oc=AdlMixLOIwNRZkIKeKtFmkhREBg6uEld68D6UeU8ZOLfnopt1KrCGCUSYDT5ikSMJy1C6IZku8TXMnzmYNhw2odH&_nc_zt=23&_nc_ht=scontent-vie1-1.xx&_nc_gid=d6WedswgV-xbWMhBdBPvvA&oh=00_Afuj3uT1eWt5Vf_h-xylGsqjPhMGitgVhbtjr9dR07dMVA&oe=69956211", caption="Éremátadás"),
            GalleryImage(id="1-3", url="https://scontent-vie1-1.xx.fbcdn.net/v/t39.30808-6/616103588_1484900556972962_5448955673734173814_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=f727a1&_nc_ohc=fdbq41Q9CIEQ7kNvwFfYSGf&_nc_oc=Admf_B4BPdLklmTjdhQG57UMMKvXRx789IrhDH0joKWciaOET6rF_86JT2uKQxHpe0Ddm2rcMY1vBwFpsuKYSLus&_nc_zt=23&_nc_ht=scontent-vie1-1.xx&_nc_gid=VgsyPZsrQ-Z7PqyrqjUtcA&oh=00_AfvHUbLs3qY4zbLSdmyIRsglSThecjiwnYrr5xqxraexZw&oe=699585F1", thumbnail="https://scontent-vie1-1.xx.fbcdn.net/v/t39.30808-6/616103588_1484900556972962_5448955673734173814_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=f727a1&_nc_ohc=fdbq41Q9CIEQ7kNvwFfYSGf&_nc_oc=Admf_B4BPdLklmTjdhQG57UMMKvXRx789IrhDH0joKWciaOET6rF_86JT2uKQxHpe0Ddm2rcMY1vBwFpsuKYSLus&_nc_zt=23&_nc_ht=scontent-vie1-1.xx&_nc_gid=VgsyPZsrQ-Z7PqyrqjUtcA&oh=00_AfvHUbLs3qY4zbLSdmyIRsglSThecjiwnYrr5xqxraexZw&oe=699585F1", caption="Éremátadás"),
            GalleryImage(id="1-4", url="https://scontent-vie1-1.xx.fbcdn.net/v/t39.30808-6/616820402_1484900593639625_7232506220084491978_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=f727a1&_nc_ohc=PRt5YRZIUFEQ7kNvwHHjURd&_nc_oc=AdmGwCwMHtzbo6WRrL80ZeeltA_E4lqS5UTUdXTZuxHfUyeenYcS7Emhk07X7iHTEiH0x2gIRJ1m2-MGbpCYN8xg&_nc_zt=23&_nc_ht=scontent-vie1-1.xx&_nc_gid=Dju3qayjeh9DK1-t3C72VQ&oh=00_AfuIVsjdxAC7UOsxyR7-romJOnVCn4MgT3z7Rhf7XsCWEw&oe=69958F61", thumbnail="https://scontent-vie1-1.xx.fbcdn.net/v/t39.30808-6/616820402_1484900593639625_7232506220084491978_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=f727a1&_nc_ohc=PRt5YRZIUFEQ7kNvwHHjURd&_nc_oc=AdmGwCwMHtzbo6WRrL80ZeeltA_E4lqS5UTUdXTZuxHfUyeenYcS7Emhk07X7iHTEiH0x2gIRJ1m2-MGbpCYN8xg&_nc_zt=23&_nc_ht=scontent-vie1-1.xx&_nc_gid=Dju3qayjeh9DK1-t3C72VQ&oh=00_AfuIVsjdxAC7UOsxyR7-romJOnVCn4MgT3z7Rhf7XsCWEw&oe=69958F61", caption="Éremátadás"),
            GalleryImage(id="1-5", url="https://scontent-vie1-1.xx.fbcdn.net/v/t39.30808-6/615966968_1484900373639647_7090054980501973447_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=f727a1&_nc_ohc=A2AZ5HD1N8UQ7kNvwHQgMQJ&_nc_oc=Adkugr7QgnmPwTCtr0YnUFFlH3gGijRV8K7JzEhaYWGxaeQI9bVuXAucd_Q2CCZW12u7CVag9c_zFutEfKBT14s4&_nc_zt=23&_nc_ht=scontent-vie1-1.xx&_nc_gid=w9RJMBvzqEg39VYXAuEEzQ&oh=00_AfuF7ApazKkSvX8t02X6XJfjP8yXjxOvKZfiSs9EBQQ4gA&oe=69956F56", thumbnail="https://scontent-vie1-1.xx.fbcdn.net/v/t39.30808-6/615966968_1484900373639647_7090054980501973447_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=f727a1&_nc_ohc=A2AZ5HD1N8UQ7kNvwHQgMQJ&_nc_oc=Adkugr7QgnmPwTCtr0YnUFFlH3gGijRV8K7JzEhaYWGxaeQI9bVuXAucd_Q2CCZW12u7CVag9c_zFutEfKBT14s4&_nc_zt=23&_nc_ht=scontent-vie1-1.xx&_nc_gid=w9RJMBvzqEg39VYXAuEEzQ&oh=00_AfuF7ApazKkSvX8t02X6XJfjP8yXjxOvKZfiSs9EBQQ4gA&oe=69956F56", caption="Éremátadás"),
        ]
    ),
    GalleryAlbum(
        id="2",
        title="Projektmunka bemutató",
        description="Diákjaink projektmunkáinak bemutatója",
        date="2025-01-15",
        cover_image="https://images.unsplash.com/photo-1531482615713-2afd69097998?w=800",
        image_count=4,
        images=[
            GalleryImage(id="2-1", url="https://images.unsplash.com/photo-1531482615713-2afd69097998?w=800", thumbnail="https://images.unsplash.com/photo-1531482615713-2afd69097998?w=400", caption="Csapatmunka"),
            GalleryImage(id="2-2", url="https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=800", thumbnail="https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=400", caption="Prezentáció"),
            GalleryImage(id="2-3", url="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800", thumbnail="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=400", caption="Együttműködés"),
            GalleryImage(id="2-4", url="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800", thumbnail="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400", caption="IT fejlesztés"),
        ]
    ),
    GalleryAlbum(
        id="3",
        title="Ballagás 2024",
        description="Ünnepélyes ballagási ceremónia",
        date="2024-05-10",
        cover_image="https://images.unsplash.com/photo-1523580846011-d3a5bc25702b?w=800",
        image_count=4,
        images=[
            GalleryImage(id="3-1", url="https://images.unsplash.com/photo-1523580846011-d3a5bc25702b?w=800", thumbnail="https://images.unsplash.com/photo-1523580846011-d3a5bc25702b?w=400", caption="Ballagás"),
            GalleryImage(id="3-2", url="https://images.unsplash.com/photo-1627556704302-624286467c65?w=800", thumbnail="https://images.unsplash.com/photo-1627556704302-624286467c65?w=400", caption="Diplomaosztó"),
            GalleryImage(id="3-3", url="https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800", thumbnail="https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=400", caption="Ünnepség"),
            GalleryImage(id="3-4", url="https://images.unsplash.com/photo-1559223607-a43f990c095c?w=800", thumbnail="https://images.unsplash.com/photo-1559223607-a43f990c095c?w=400", caption="Csoportkép"),
        ]
    ),
    GalleryAlbum(
        id="4",
        title="Sportverseny",
        description="Iskolai sportversenyek és eredmények",
        date="2024-11-20",
        cover_image="https://images.unsplash.com/photo-1461896836934- voices=true-03bf60d-a05f-4b4e-a573-24508a0ee33e?w=800",
        image_count=3,
        images=[
            GalleryImage(id="4-1", url="https://bm-pataky.cms.intezmeny.edir.hu/uploads/Baker_Hughes_Manhertz_Gergo_9_resized_e58b431528.jpg", thumbnail="https://bm-pataky.cms.intezmeny.edir.hu/uploads/Baker_Hughes_Manhertz_Gergo_9_resized_e58b431528.jpg", caption="Távközlés orientáció terem"),
            GalleryImage(id="4-2", url="https://scontent-vie1-1.xx.fbcdn.net/v/t39.30808-6/622919231_1421246323349398_2086000057285671729_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=127cfc&_nc_ohc=RsqCM_U5qE4Q7kNvwFnqb8g&_nc_oc=AdnF1LH-Y5U68riHuOZb2IerkQHuig5UbNDUN9ioAm3RR9qp_2LP2C8cfw1Z-6Y96VrjWcaFrGC9PQt0gQ4Ws5lu&_nc_zt=23&_nc_ht=scontent-vie1-1.xx&_nc_gid=-NuQIgYIps8F1pK0rytCvA&oh=00_AfsZblM8vobfGHHHizG4XQjPJfc-sQqQfUBhBzsNXu_jMg&oe=69958B84", thumbnail="https://scontent-vie1-1.xx.fbcdn.net/v/t39.30808-6/622919231_1421246323349398_2086000057285671729_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=127cfc&_nc_ohc=RsqCM_U5qE4Q7kNvwFnqb8g&_nc_oc=AdnF1LH-Y5U68riHuOZb2IerkQHuig5UbNDUN9ioAm3RR9qp_2LP2C8cfw1Z-6Y96VrjWcaFrGC9PQt0gQ4Ws5lu&_nc_zt=23&_nc_ht=scontent-vie1-1.xx&_nc_gid=-NuQIgYIps8F1pK0rytCvA&oh=00_AfsZblM8vobfGHHHizG4XQjPJfc-sQqQfUBhBzsNXu_jMg&oe=69958B84", caption="Angol Kahoot verseny"),
            GalleryImage(id="4-3", url="https://images.unsplash.com/photo-1587280501635-68a0e82cd5ff?w=800", thumbnail="https://images.unsplash.com/photo-1587280501635-68a0e82cd5ff?w=400", caption="Éremátadás"),
        ]
    ),
]

# Campus Map data
class Room(BaseModel):
    id: str
    name: str
    floor: int
    building: str
    type: str  # classroom, lab, office, facility
    description: Optional[str] = None

class Building(BaseModel):
    id: str
    name: str
    code: str
    floors: int
    description: str
    rooms: List[Room]

CAMPUS_BUILDINGS = [
    Building(
        id="1",
        name="Főépület",
        code="A",
        floors=3,
        description="Adminisztráció, vezetőség, közismereti tantermek",
        rooms=[
            Room(id="A-001", name="Porta", floor=0, building="A", type="facility", description="Beléptetés, információ"),
            Room(id="A-002", name="Titkárság", floor=0, building="A", type="office", description="Ügyintézés"),
            Room(id="A-101", name="Igazgatói iroda", floor=1, building="A", type="office"),
            Room(id="A-102", name="Tanári szoba", floor=1, building="A", type="office"),
            Room(id="A-103", name="Fizika labor", floor=1, building="A", type="lab", description="Fizikai kísérletek"),
            Room(id="A-104", name="Kémia labor", floor=1, building="A", type="lab", description="Kémiai kísérletek"),
            Room(id="A-105", name="Elektronika műhely", floor=1, building="A", type="lab", description="Elektronikai gyakorlat"),
            Room(id="A-201", name="101-es tanterem", floor=2, building="A", type="classroom"),
            Room(id="A-202", name="102-es tanterem", floor=2, building="A", type="classroom"),
            Room(id="A-203", name="103-as tanterem", floor=2, building="A", type="classroom"),
            Room(id="A-301", name="Díszterem", floor=3, building="A", type="facility", description="Rendezvények, ünnepségek"),
        ]
    ),
    Building(
        id="2",
        name="Informatikai épület",
        code="B",
        floors=2,
        description="Számítógéptermek, informatikai laborok",
        rooms=[
            Room(id="B-001", name="Szerviz", floor=0, building="B", type="facility", description="IT eszközök javítása"),
            Room(id="B-101", name="Gépterem 1", floor=1, building="B", type="lab", description="30 munkaállomás"),
            Room(id="B-102", name="Gépterem 2", floor=1, building="B", type="lab", description="30 munkaállomás"),
            Room(id="B-103", name="Hálózati labor", floor=1, building="B", type="lab", description="Cisco hálózati eszközök"),
            Room(id="B-201", name="Gépterem 3", floor=2, building="B", type="lab", description="25 munkaállomás"),
            Room(id="B-202", name="Gépterem 4", floor=2, building="B", type="lab", description="25 munkaállomás"),
            Room(id="B-203", name="Programozói labor", floor=2, building="B", type="lab", description="Fejlesztői környezet"),
            Room(id="B-205", name="Adatbázis labor", floor=2, building="B", type="lab", description="SQL gyakorlat"),
            Room(id="B-207", name="Mobil labor", floor=2, building="B", type="lab", description="Mobilfejlesztés"),
        ]
    ),
    Building(
        id="3",
        name="Közismereti épület",
        code="C",
        floors=3,
        description="Nyelvi termek, humán tantárgyak",
        rooms=[
            Room(id="C-101", name="Könyvtár", floor=1, building="C", type="facility", description="Tanulás, olvasás"),
            Room(id="C-102", name="Nyelvi labor", floor=1, building="C", type="lab", description="Nyelvtanulás"),
            Room(id="C-104", name="Kémia terem", floor=1, building="C", type="classroom"),
            Room(id="C-201", name="Magyar terem", floor=2, building="C", type="classroom"),
            Room(id="C-202", name="Történelem terem", floor=2, building="C", type="classroom"),
            Room(id="C-301", name="Irodalom tanári", floor=3, building="C", type="office"),
            Room(id="C-302", name="Matematika terem", floor=3, building="C", type="classroom"),
            Room(id="C-303", name="Történelem tanári", floor=3, building="C", type="office"),
            Room(id="C-305", name="Angol terem", floor=3, building="C", type="classroom"),
        ]
    ),
    Building(
        id="4",
        name="Sportlétesítmény",
        code="S",
        floors=1,
        description="Tornaterem, sportpályák",
        rooms=[
            Room(id="S-001", name="Tornaterem", floor=0, building="S", type="facility", description="Testnevelés órák"),
            Room(id="S-002", name="Öltöző - fiú", floor=0, building="S", type="facility"),
            Room(id="S-003", name="Öltöző - lány", floor=0, building="S", type="facility"),
            Room(id="S-004", name="Konditerem", floor=0, building="S", type="facility", description="Edzőterem"),
            Room(id="S-005", name="Sportudvar", floor=0, building="S", type="facility", description="Kültéri pályák"),
        ]
    ),
    Building(
        id="5",
        name="Menza épület",
        code="M",
        floors=1,
        description="Étkezés, büfé",
        rooms=[
            Room(id="M-001", name="Ebédlő", floor=0, building="M", type="facility", description="Ebédidő: 11:30-14:00"),
            Room(id="M-002", name="Büfé", floor=0, building="M", type="facility", description="Nyitva: 7:00-15:00"),
            Room(id="M-003", name="Konyha", floor=0, building="M", type="facility"),
        ]
    ),
]

EVENTS = [
    Event(id="1", title="Nyílt nap", date="2025-02-15", description="Ismerkedj meg iskolánkkal! Programok, bemutatók, tájékoztató.", location="Pataky Technikum"),
    Event(id="2", title="Felvételi időszak kezdete", date="2025-02-20", description="A központi írásbeli felvételi vizsga időpontja.", location="Pataky Technikum"),
    Event(id="3", title="Szülői értekezlet", date="2025-03-05", description="Tájékoztató a 2024/2025-ös tanév második félévéről.", location="Pataky Technikum"),
    Event(id="4", title="Római tanulmányi út", date="2025-03-17", description="4 napos tanulmányi út Rómába.", location="Róma, Olaszország"),
    Event(id="5", title="Érettségi szóbeli", date="2025-06-02", description="Szóbeli érettségi vizsgák kezdete.", location="Pataky Technikum"),
]

QUICK_LINKS = [
    {"id": "1", "title": "KRÉTA", "description": "E-napló belépés", "url": "https://bmszc-pataky.e-kreta.hu/", "icon": "book"},
    {"id": "2", "title": "Órarend", "description": "Tanóra beosztás", "url": "https://pataky.hu/tanuloinknak/tanev-rendje", "icon": "calendar"},
    {"id": "3", "title": "Menza", "description": "Étkezési információk", "url": "https://pataky.hu/p/etkezes", "icon": "restaurant"},
    {"id": "4", "title": "Duális képzés", "description": "Ipari partnerek", "url": "https://pataky.hu/p/dualis-kepzes", "icon": "business"},
]

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Pataky Technikum API"}

@api_router.get("/school-info")
async def get_school_info():
    return SCHOOL_INFO

@api_router.get("/contact")
async def get_contact():
    return CONTACT_INFO

@api_router.get("/news", response_model=List[NewsArticle])
async def get_news():
    return NEWS_ARTICLES

@api_router.get("/news/{news_id}", response_model=NewsArticle)
async def get_news_by_id(news_id: str):
    for article in NEWS_ARTICLES:
        if article.id == news_id:
            return article
    return None

@api_router.get("/courses", response_model=List[Course])
async def get_courses():
    return COURSES

@api_router.get("/courses/{course_type}")
async def get_courses_by_type(course_type: str):
    return [c for c in COURSES if c.type == course_type]

@api_router.get("/staff", response_model=List[StaffMember])
async def get_staff():
    return STAFF_MEMBERS

@api_router.get("/events", response_model=List[Event])
async def get_events():
    return EVENTS

@api_router.get("/quick-links")
async def get_quick_links():
    return QUICK_LINKS

@api_router.get("/teachers", response_model=List[Teacher])
async def get_teachers():
    return TEACHERS

@api_router.get("/teachers/search")
async def search_teachers(q: str = ""):
    if not q:
        return TEACHERS
    q_lower = q.lower()
    return [t for t in TEACHERS if q_lower in t.name.lower() or q_lower in t.subject.lower() or q_lower in t.department.lower()]

# 1. Csak az adatokat adja vissza (ez a jó gyakorlat)
@api_router.get("/menu", response_model=List[DailyMenu])
async def get_menu():
    return WEEKLY_MENU

# 2. Ez végzi a tényleges értesítést (ezt hívd meg, ha üzenni akarsz)
@api_router.post("/send-menu-push")
async def send_menu_push():
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_menu = next((item for item in WEEKLY_MENU if item.date == today_str), None)

    if today_menu:
        title = f"Mai menü - {today_menu.day} 🍴"
        body = f"Leves: {today_menu.soup.name}\nFőétel: {today_menu.main_course.name}"
    else:
        title = "Pataky Menza 🍴"
        body = "Nézd meg a heti menüt az alkalmazásban!"

    return send_push_to_all(title, body)



@api_router.get("/gallery")
async def get_gallery():
    return GALLERY_ALBUMS

@api_router.get("/gallery/{album_id}")
async def get_gallery_album(album_id: str):
    for album in GALLERY_ALBUMS:
        if album.id == album_id:
            return album
    return None

@api_router.get("/campus")
async def get_campus():
    return CAMPUS_BUILDINGS

@api_router.get("/campus/{building_id}")
async def get_building(building_id: str):
    for building in CAMPUS_BUILDINGS:
        if building.id == building_id:
            return building
    return None

@api_router.get("/rooms/search")
async def search_rooms(q: str = ""):
    if not q:
        return []
    q_lower = q.lower()
    results = []
    for building in CAMPUS_BUILDINGS:
        for room in building.rooms:
            if q_lower in room.name.lower() or q_lower in room.id.lower():
                results.append({"room": room, "building": building.name, "building_code": building.code})
    return results

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@api_router.get("/rooms/search")
async def search_rooms(q: str = ""):
    if not q:
        return []
    results = []
    q_lower = q.lower()
    for building in CAMPUS_BUILDINGS:
        for room in building.rooms:
            if q_lower in room.name.lower() or (room.description and q_lower in room.description.lower()):
                results.append(room)
    return results

# FONTOS: A router regisztrálása az app-hoz
app.include_router(api_router)

# Belépési pont a lokális futtatáshoz
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
