"""
Script to populate Azure PostgreSQL database with sample gaming forum data
Run with: python populate_azure_db.py
"""

import sys
import os
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
import random
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import Base
from backend.models import User, Game, Post
from backend.sentiment import sentiment_analyzer

# Get Azure database URL from environment or use default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://pgadmin:YourPassword@gaming-forum-prod-psql-xxxxx.postgres.database.azure.com:5432/forum_db?sslmode=require"
)

print(f"Connecting to: {DATABASE_URL.split('@')[1].split('/')[0]}")  # Show host only

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Expanded list of 60 popular games
GAMES_DATA = [
    # Action-Adventure
    ("The Last of Us Part II", "Action-Adventure", "Post-apocalyptic action-adventure with emotional storytelling"),
    ("God of War Ragnarök", "Action-Adventure", "Norse mythology action game with Kratos and Atreus"),
    ("Spider-Man 2", "Action-Adventure", "Superhero action game featuring Peter Parker and Miles Morales"),
    ("Zelda: Tears of the Kingdom", "Action-Adventure", "Open-world adventure sequel to Breath of the Wild"),
    ("Uncharted 4", "Action-Adventure", "Treasure hunting adventure with Nathan Drake"),
    ("Ghost of Tsushima", "Action-Adventure", "Samurai epic set in feudal Japan"),
    ("Red Dead Redemption 2", "Action-Adventure", "Western epic with Arthur Morgan"),
    ("Assassin's Creed Valhalla", "Action-Adventure", "Viking adventure in medieval England"),
    
    # RPG
    ("Elden Ring", "Action RPG", "Open-world souls-like from FromSoftware"),
    ("Baldurs Gate 3", "RPG", "Fantasy role-playing game based on D&D 5e"),
    ("Cyberpunk 2077", "Action RPG", "Open-world cyberpunk RPG in Night City"),
    ("Final Fantasy XVI", "Action RPG", "Fantasy action RPG with real-time combat"),
    ("Starfield", "Action RPG", "Space exploration RPG from Bethesda"),
    ("Hogwarts Legacy", "Action RPG", "Harry Potter universe open-world RPG"),
    ("The Witcher 3", "Action RPG", "Monster hunting in a dark fantasy world"),
    ("Skyrim", "Action RPG", "Classic open-world fantasy RPG"),
    ("Dark Souls III", "Action RPG", "Challenging souls-like action RPG"),
    ("Persona 5 Royal", "JRPG", "Stylish Japanese RPG with turn-based combat"),
    ("Dragon Age: Inquisition", "RPG", "Fantasy RPG with tactical combat"),
    ("Mass Effect Legendary", "Action RPG", "Sci-fi RPG trilogy remastered"),
    
    # FPS/Shooter
    ("Call of Duty: MW3", "FPS", "Modern military first-person shooter"),
    ("Battlefield 2042", "FPS", "Large-scale multiplayer warfare"),
    ("Apex Legends", "Battle Royale", "Hero-based battle royale shooter"),
    ("Valorant", "Tactical Shooter", "5v5 tactical hero shooter"),
    ("Counter-Strike 2", "FPS", "Competitive tactical shooter"),
    ("Overwatch 2", "Hero Shooter", "Team-based hero shooter"),
    ("Destiny 2", "Looter Shooter", "Sci-fi looter shooter MMO"),
    ("Halo Infinite", "FPS", "Sci-fi arena shooter"),
    
    # Sports/Racing
    ("FC 24", "Sports", "Realistic football simulation"),
    ("NBA 2K24", "Sports", "Basketball simulation game"),
    ("Gran Turismo 7", "Racing", "Realistic racing simulator"),
    ("Forza Horizon 5", "Racing", "Open-world arcade racing"),
    ("F1 23", "Racing", "Formula 1 racing simulation"),
    
    # Strategy
    ("Civilization VI", "Strategy", "Turn-based civilization builder"),
    ("Total War: Warhammer III", "Strategy", "Fantasy real-time strategy"),
    ("XCOM 2", "Tactical Strategy", "Turn-based tactical alien combat"),
    ("Age of Empires IV", "RTS", "Historical real-time strategy"),
    
    # Horror/Survival
    ("Resident Evil 4 Remake", "Survival Horror", "Reimagined survival horror classic"),
    ("Dead Space Remake", "Survival Horror", "Sci-fi horror in space"),
    ("Alan Wake 2", "Horror", "Psychological horror thriller"),
    ("The Callisto Protocol", "Horror", "Space prison horror game"),
    
    # Indie/Platformer
    ("Hollow Knight", "Metroidvania", "Hand-drawn action platformer"),
    ("Celeste", "Platformer", "Challenging precision platformer"),
    ("Hades", "Roguelike", "Greek mythology roguelike dungeon crawler"),
    ("Stardew Valley", "Simulation", "Farming and life simulation"),
    ("Terraria", "Sandbox", "2D sandbox adventure game"),
    ("Dead Cells", "Roguelike", "Action platformer roguelike"),
    
    # Multiplayer/Online
    ("Fortnite", "Battle Royale", "Popular battle royale shooter"),
    ("League of Legends", "MOBA", "Competitive 5v5 MOBA"),
    ("Dota 2", "MOBA", "Complex competitive MOBA"),
    ("Rocket League", "Sports", "Car soccer competitive game"),
    ("Among Us", "Social Deduction", "Multiplayer social deduction game"),
    ("Fall Guys", "Party", "Chaotic obstacle course party game"),
    ("Sea of Thieves", "Adventure", "Pirate multiplayer adventure"),
    
    # Simulation
    ("Microsoft Flight Simulator", "Simulation", "Ultra-realistic flight simulation"),
    ("Cities: Skylines", "Simulation", "City building simulation"),
    ("The Sims 4", "Life Sim", "Life simulation game"),
    ("Euro Truck Simulator 2", "Simulation", "Truck driving simulation"),
    
    # Other
    ("Minecraft", "Sandbox", "Block-building creative sandbox"),
    ("Grand Theft Auto V", "Action", "Open-world crime action game"),
    ("Death Stranding", "Adventure", "Unique delivery-based adventure"),
]

# Expanded usernames (100 users)
USERNAMES = [
    "ProGamer2024", "CasualPlayer99", "RPGFanatic", "FPSMaster", "IndieGameLover",
    "RetroGamer", "SpeedRunner420", "StrategyKing", "PuzzleSolver", "HorrorFan",
    "OpenWorldExplorer", "CompetitiveGamer", "StoryEnthusiast", "GraphicsSnob", "BudgetGamer",
    "NintendoFan", "PCMasterRace", "ConsoleCowboy", "MobileGamer", "VRPioneer",
    "AchievementHunter", "ModEnthusiast", "eSportsWatcher", "LoreMaster", "MinMaxer",
    "FilmGrainHater", "SoundtrackLover", "CouchCoopFan", "SoloPlayer", "RaidLeader",
    "TwitchStreamer", "DiscordMod", "WikiEditor", "GuideWriter", "BugReporter",
    "EarlyAdopter", "PatientGamer", "SaleHunter", "BacklogWarrior", "100Percenter",
    "PlatinumTrophy", "NoobSlayer", "TeamPlayer", "LoneWolf", "RageQuitter",
    "ChillGamer", "HardcorePlayer", "PhotoModeAddict", "EmoteLover", "SkinCollector",
    "GuildMaster", "DPSMain", "HealerLife", "TankSpecialist", "PvPLegend",
    "QuestCompleter", "EasterEggFinder", "SecretHunter", "GlitchExploiter", "MetaBreaker",
    "Theorycrafter", "BuildOptimizer", "ResourceHoarder", "TradeExpert", "MarketWhale",
    "FreeToPlayKing", "PayToWinner", "SkinAddict", "CosmeticCollector", "BattlePassGrinder",
    "RankedClimber", "CasualOnly", "SoloQueue", "FullParty", "FlexPicker",
    "OneTricker", "TierListObsessed", "PatchNotesReader", "MetaSlave", "OffMetaHero",
    "StreamSniper", "ClipChaser", "HighlightReel", "MontageEditor", "ContentCreator",
    "TutorialSkipper", "NeverReadPatch", "AlwaysComplaining", "PositiveVibes", "ToxicPlayer",
    "AFKMaster", "DCDisconnect", "LagBlamer", "PingWarrior", "ServerBlamer",
    "RNGBlessed", "CriticalHitGod", "DodgeRollPro", "ParryKing", "BlockChamp",
    "ComboMaster", "InputReader", "FramePerfect", "TechChaser", "WaveDasher",
]

# Review templates
POSITIVE_REVIEWS = [
    ("Amazing masterpiece!", "This game is absolutely incredible! Best {genre} I've played in years. The graphics are stunning and gameplay is perfect. 10/10 would recommend!"),
    ("Exceeded all expectations", "Wow! This game blew my mind. The story is engaging, mechanics are smooth, and the world feels alive. Can't stop playing!"),
    ("Pure perfection", "Everything about this game is perfect. From the soundtrack to the level design, it's a masterpiece. Worth every penny!"),
    ("Absolutely love it!", "I'm completely addicted! The gameplay loop is so satisfying. Best purchase I've made this year. Highly recommended!"),
    ("Game of the year material", "This is GOTY material for sure! Incredible attention to detail, fantastic combat, and amazing atmosphere."),
    ("Blown away by quality", "The quality is insane! Every aspect is polished to perfection. The devs really outdid themselves."),
    ("Best {genre} ever!", "Hands down the best {genre} game ever made. Sets a new standard for the industry."),
    ("Can't put it down", "I've been playing non-stop! The game is so engaging and fun. Time just flies by when I play."),
    ("Absolutely stunning", "Visually stunning and mechanically brilliant. This game is a work of art!"),
    ("10/10 masterpiece", "Perfect 10/10. No flaws, just pure gaming excellence. A must-play for everyone!"),
]

NEGATIVE_REVIEWS = [
    ("Extremely disappointed", "Very disappointed with this game. Buggy, boring, and not worth the price. Should have waited for reviews."),
    ("Total waste of money", "Terrible experience. The game is broken, unfinished, and frustrating. Complete waste of $60."),
    ("Boring and repetitive", "So boring! Same thing over and over. Got old after 2 hours. Regret buying this."),
    ("Buggy mess", "This game is a buggy mess! Constant crashes, poor optimization, game-breaking bugs everywhere. Unplayable!"),
    ("Not worth it", "Overhyped and underwhelming. The gameplay is shallow and the story is weak. Skip this one."),
    ("Huge letdown", "Such a letdown after all the hype. Poor mechanics, terrible AI, dated graphics. Very disappointing."),
    ("Refunded immediately", "Played for 30 minutes and refunded. Awful controls, bad design, not fun at all."),
    ("Worst {genre} ever", "Probably the worst {genre} I've ever played. Everything feels cheap and rushed."),
]

NEUTRAL_REVIEWS = [
    ("It's okay I guess", "The game is okay. Not great, not terrible. Has some fun moments but also frustrating parts. 6/10."),
    ("Mixed feelings", "I have mixed feelings about this. Some aspects are good, others need work. Might improve with patches."),
    ("Average experience", "Pretty average {genre}. Nothing special but not bad either. If you like the genre, might be worth it on sale."),
    ("Has potential", "The game has potential but feels unfinished. Good ideas but poor execution. Maybe worth it after updates."),
    ("Could be better", "It's alright but could be much better. Some good parts but also many issues that hold it back."),
    ("Not for everyone", "Not a bad game but definitely not for everyone. If you're a fan of {genre}, you might enjoy it."),
]


def generate_sample_data():
    """Generate sample data with 60 games and 1000+ posts"""
    db = SessionLocal()
    
    try:
        print("🎮 Gaming Forum Data Generator - Azure Edition")
        print("=" * 60)
        print(f"📍 Target: Azure PostgreSQL")
        print()
        
        # Create tables if they don't exist
        print("🔧 Creating tables if needed...")
        Base.metadata.create_all(bind=engine)
        print("✓ Tables ready")
        
        # Create/update games
        print("\n🎯 Creating 60 games...")
        games_created = 0
        existing_games = {g[0] for g in db.query(Game.name).all()}
        
        for name, genre, description in GAMES_DATA:
            if name not in existing_games:
                game = Game(
                    name=name,
                    genre=genre,
                    description=description,
                    image_url=f"https://placehold.co/300x400/21808d/ffffff?text={name.replace(' ', '+')}"
                )
                db.add(game)
                games_created += 1
        
        db.commit()
        print(f"✓ Created {games_created} new games (Total: {len(GAMES_DATA)} games)")
        
        # Create users
        print("\n👥 Creating 100 users...")
        existing_users = {u[0] for u in db.query(User.username).all()}
        new_users = []
        
        for username in USERNAMES:
            if username not in existing_users:
                user = User(
                    username=username,
                    email=f"{username.lower()}@example.com"
                )
                new_users.append(user)
        
        if new_users:
            db.add_all(new_users)
            db.commit()
        print(f"✓ Created {len(new_users)} new users (Total: {len(USERNAMES)} users)")
        
        # Get all games and users
        all_games = db.query(Game).all()
        all_users = db.query(User).all()
        
        if not all_users:
            print("❌ No users found! Check database connection.")
            return
        
        # Generate 1000 posts
        print("\n📝 Generating 1000 posts with sentiment analysis...")
        print("   (This will take 10-15 minutes...)\n")
        
        posts_created = 0
        target_posts = 1000
        
        # Distribution: 40% positive, 35% negative, 25% neutral
        num_positive = int(target_posts * 0.40)
        num_negative = int(target_posts * 0.35)
        num_neutral = target_posts - num_positive - num_negative
        
        review_types = (
            [('positive', POSITIVE_REVIEWS)] * num_positive +
            [('negative', NEGATIVE_REVIEWS)] * num_negative +
            [('neutral', NEUTRAL_REVIEWS)] * num_neutral
        )
        random.shuffle(review_types)
        
        for i, (sentiment_type, review_templates) in enumerate(review_types):
            # Random game and user
            game = random.choice(all_games)
            user = random.choice(all_users)
            
            # Random review template
            title, content_template = random.choice(review_templates)
            content = content_template.format(genre=game.genre)
            
            # Random timestamp (last 60 days)
            days_ago = random.randint(0, 60)
            hours_ago = random.randint(0, 23)
            created_at = datetime.now() - timedelta(days=days_ago, hours=hours_ago)
            
            # Analyze sentiment
            sentiment_result = sentiment_analyzer.analyze(content)
            
            # Create post
            post = Post(
                user_id=user.id,
                game_id=game.id,
                title=title,
                content=content,
                sentiment_score=sentiment_result['sentiment_score'],
                sentiment_label=sentiment_result['label'],
                confidence=sentiment_result['confidence'],
                created_at=created_at,
                updated_at=created_at
            )
            
            db.add(post)
            posts_created += 1
            
            # Commit every 50 posts and show progress
            if posts_created % 50 == 0:
                db.commit()
                progress = (posts_created / target_posts) * 100
                print(f"  ✓ Progress: {posts_created}/{target_posts} ({progress:.0f}%)")
        
        db.commit()
        print(f"\n✅ Successfully created {posts_created} posts!")
        
        # Show detailed statistics
        print("\n📊 Final Statistics:")
        print("=" * 60)
        
        # Overall stats
        total_posts = db.query(func.count(Post.id)).scalar()
        total_games = db.query(func.count(Game.id)).scalar()
        total_users = db.query(func.count(User.id)).scalar()
        avg_sentiment = db.query(func.avg(Post.sentiment_score)).scalar()
        
        positive_count = db.query(func.count(Post.id)).filter(Post.sentiment_label == 'POSITIVE').scalar()
        negative_count = db.query(func.count(Post.id)).filter(Post.sentiment_label == 'NEGATIVE').scalar()
        neutral_count = db.query(func.count(Post.id)).filter(Post.sentiment_label == 'NEUTRAL').scalar()
        
        print(f"Total Games: {total_games}")
        print(f"Total Users: {total_users}")
        print(f"Total Posts: {total_posts}")
        print(f"Average Sentiment: {avg_sentiment:.3f}")
        print(f"Positive: {positive_count} ({positive_count/total_posts*100:.1f}%)")
        print(f"Negative: {negative_count} ({negative_count/total_posts*100:.1f}%)")
        print(f"Neutral: {neutral_count} ({neutral_count/total_posts*100:.1f}%)")
        
        print("\nData generation complete!")
        print(f"Check your app at: https://gaming-forum-prod-frontend.*.azurecontainerapps.io")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    generate_sample_data()
