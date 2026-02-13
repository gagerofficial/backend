from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


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
    StaffMember(id="1", name="Igazgató", position="Intézményvezető", department="Vezetőség", email="igazgato@pataky.hu"),
    StaffMember(id="2", name="Informatika Tanszék", position="Oktatási egység", department="Informatika"),
    StaffMember(id="3", name="Elektronika Tanszék", position="Oktatási egység", department="Elektronika"),
    StaffMember(id="4", name="Közismereti Tanszék", position="Oktatási egység", department="Közismeret"),
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
    Teacher(id="1", name="Dr. Kovács Péter", subject="Programozás, Webfejlesztés", department="Informatika", email="kovacs.peter@pataky.hu", office="B épület 201", consultation_hours="Kedd 14:00-16:00"),
    Teacher(id="2", name="Nagy Éva", subject="Hálózatok, Rendszerüzemeltetés", department="Informatika", email="nagy.eva@pataky.hu", office="B épület 203", consultation_hours="Szerda 13:00-15:00"),
    Teacher(id="3", name="Szabó János", subject="Elektronika, Áramkörök", department="Elektronika", email="szabo.janos@pataky.hu", office="A épület 105", consultation_hours="Hétfő 14:00-16:00"),
    Teacher(id="4", name="Tóth Mária", subject="Matematika, Fizika", department="Közismeret", email="toth.maria@pataky.hu", office="C épület 302", consultation_hours="Csütörtök 13:00-15:00"),
    Teacher(id="5", name="Horváth László", subject="Magyar nyelv és irodalom", department="Közismeret", email="horvath.laszlo@pataky.hu", office="C épület 301", consultation_hours="Péntek 12:00-14:00"),
    Teacher(id="6", name="Kiss Andrea", subject="Angol nyelv", department="Közismeret", email="kiss.andrea@pataky.hu", office="C épület 305", consultation_hours="Kedd 12:00-14:00"),
    Teacher(id="7", name="Molnár Gábor", subject="Adatbáziskezelés, SQL", department="Informatika", email="molnar.gabor@pataky.hu", office="B épület 205", consultation_hours="Szerda 14:00-16:00"),
    Teacher(id="8", name="Varga Katalin", subject="Történelem, Társadalomismeret", department="Közismeret", email="varga.katalin@pataky.hu", office="C épület 303", consultation_hours="Hétfő 13:00-15:00"),
    Teacher(id="9", name="Fekete Zoltán", subject="Elektrotechnika, Villamos gépek", department="Elektronika", email="fekete.zoltan@pataky.hu", office="A épület 107", consultation_hours="Csütörtök 14:00-16:00"),
    Teacher(id="10", name="Balogh Eszter", subject="Testnevelés", department="Közismeret", email="balogh.eszter@pataky.hu", office="Tornaterem", consultation_hours="Péntek 10:00-12:00"),
    Teacher(id="11", name="Papp Béla", subject="Mobil alkalmazásfejlesztés", department="Informatika", email="papp.bela@pataky.hu", office="B épület 207", consultation_hours="Kedd 15:00-17:00"),
    Teacher(id="12", name="Simon Ágnes", subject="Kémia", department="Közismeret", email="simon.agnes@pataky.hu", office="C épület 104", consultation_hours="Szerda 12:00-14:00"),
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
        date="2025-02-10",
        soup=MenuItem(name="Húsleves cérnametélttel", allergens=["glutén", "tojás"]),
        main_course=MenuItem(name="Rántott csirkemell rizzsel és tartármártással", allergens=["glutén", "tojás", "tej"]),
        dessert=MenuItem(name="Almás pite", allergens=["glutén", "tej", "tojás"])
    ),
    DailyMenu(
        day="Kedd",
        date="2025-02-11",
        soup=MenuItem(name="Paradicsomleves betűtésztával", allergens=["glutén"]),
        main_course=MenuItem(name="Sertéspörkölt galuskával", allergens=["glutén", "tojás"]),
        dessert=MenuItem(name="Túrógombóc", allergens=["tej", "tojás", "glutén"])
    ),
    DailyMenu(
        day="Szerda",
        date="2025-02-12",
        soup=MenuItem(name="Zöldborsóleves", allergens=["tej"]),
        main_course=MenuItem(name="Töltött paprika főtt burgonyával", allergens=["glutén"]),
        dessert=MenuItem(name="Gyümölcssaláta")
    ),
    DailyMenu(
        day="Csütörtök",
        date="2025-02-13",
        soup=MenuItem(name="Gulyásleves", allergens=["glutén"]),
        main_course=MenuItem(name="Milánói spagetti sajttal", allergens=["glutén", "tej"]),
        dessert=MenuItem(name="Palacsinta lekváros", allergens=["glutén", "tej", "tojás"])
    ),
    DailyMenu(
        day="Péntek",
        date="2025-02-14",
        soup=MenuItem(name="Halászlé", allergens=["hal"]),
        main_course=MenuItem(name="Rántott sajt hasábburgonyával", allergens=["glutén", "tej", "tojás"]),
        dessert=MenuItem(name="Krémes", allergens=["glutén", "tej", "tojás"])
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
        title="Nyílt Nap 2025",
        description="Betekintés az iskola életébe a leendő diákok és szülők számára",
        date="2025-01-25",
        cover_image="https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800",
        image_count=4,
        images=[
            GalleryImage(id="1-1", url="https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800", thumbnail="https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400", caption="Iskolai bemutató"),
            GalleryImage(id="1-2", url="https://images.unsplash.com/photo-1562774053-701939374585?w=800", thumbnail="https://images.unsplash.com/photo-1562774053-701939374585?w=400", caption="Informatika labor"),
            GalleryImage(id="1-3", url="https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=800", thumbnail="https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=400", caption="Tanterem"),
            GalleryImage(id="1-4", url="https://images.unsplash.com/photo-1509062522246-3755977927d7?w=800", thumbnail="https://images.unsplash.com/photo-1509062522246-3755977927d7?w=400", caption="Diákok"),
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
            GalleryImage(id="4-1", url="https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=800", thumbnail="https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=400", caption="Tornaterem"),
            GalleryImage(id="4-2", url="https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=800", thumbnail="https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=400", caption="Focimeccs"),
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

@api_router.get("/menu")
async def get_menu():
    return WEEKLY_MENU

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
