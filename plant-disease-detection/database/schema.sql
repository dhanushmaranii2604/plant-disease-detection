-- ============================================
-- Plant Disease Detection System - Database Schema
-- Visual Plant Disease Diagnosis Using AI: DL and ML Approaches
-- Student: Dhanush M | USN: 1NT23MC016 | NMIT Bengaluru
-- ============================================

CREATE DATABASE IF NOT EXISTS plant_disease_db;
USE plant_disease_db;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Predictions table
CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    image_path VARCHAR(255),
    disease_name VARCHAR(150) NOT NULL,
    confidence FLOAT NOT NULL,
    model_used VARCHAR(50) DEFAULT 'MobileNet',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Diseases table (with remedies)
CREATE TABLE IF NOT EXISTS diseases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    disease_name VARCHAR(150) NOT NULL UNIQUE,
    plant_name VARCHAR(100),
    causes TEXT,
    symptoms TEXT,
    organic_remedy TEXT,
    chemical_remedy TEXT,
    prevention_tips TEXT
);

-- ============================================
-- Seed Disease Data
-- ============================================
INSERT INTO diseases (disease_name, plant_name, causes, symptoms, organic_remedy, chemical_remedy, prevention_tips) VALUES
('Apple___Apple_scab', 'Apple', 'Fungus Venturia inaequalis', 'Olive-green to brown spots on leaves and fruit', 'Neem oil spray, sulfur dust weekly', 'Fungicides containing myclobutanil or captan', 'Remove fallen leaves, prune for air circulation, plant resistant varieties'),
('Apple___Black_rot', 'Apple', 'Fungus Botryosphaeria obtusa', 'Brown circular lesions on leaves, mummified fruit', 'Copper fungicides (organic), remove infected wood', 'Propiconazole or thiophanate-methyl', 'Remove infected branches, avoid overhead watering, proper sanitation'),
('Apple___Cedar_apple_rust', 'Apple', 'Fungus Gymnosporangium juniperi-virginianae', 'Bright orange spots on upper leaf surface', 'Sulfur spray, neem oil early season', 'Myclobutanil or triadimefon fungicides at bud break', 'Remove cedar trees nearby, plant resistant apple varieties'),
('Apple___healthy', 'Apple', 'No disease detected', 'Leaf appears healthy with no visible symptoms', 'Continue regular care and monitoring', 'No treatment needed', 'Maintain proper watering, fertilization and pruning'),
('Cherry_(including_sour)___Powdery_mildew', 'Cherry', 'Fungus Podosphaera clandestina', 'White powdery coating on leaves and young shoots', 'Milk spray (1:9 ratio), baking soda solution, neem oil', 'Sulfur or potassium bicarbonate fungicides', 'Prune for air flow, avoid wet leaves, plant resistant varieties'),
('Cherry_(including_sour)___healthy', 'Cherry', 'No disease detected', 'Leaf appears healthy with no visible symptoms', 'Continue regular care and monitoring', 'No treatment needed', 'Maintain proper watering and regular pruning'),
('Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn', 'Fungus Cercospora zeae-maydis', 'Rectangular gray to tan lesions parallel to leaf veins', 'Crop rotation, remove infected debris, compost tea', 'Strobilurin or triazole fungicides', 'Plant tolerant hybrids, proper spacing for airflow, crop rotation'),
('Corn_(maize)___Common_rust_', 'Corn', 'Fungus Puccinia sorghi', 'Small, oval, brick-red pustules on both leaf surfaces', 'Neem oil, compost tea spray early morning', 'Azoxystrobin or pyraclostrobin', 'Plant resistant hybrids, early planting, crop rotation'),
('Corn_(maize)___Northern_Leaf_Blight', 'Corn', 'Fungus Exserohilum turcicum', 'Long, cigar-shaped gray-green lesions on leaves', 'Garlic spray, copper fungicide, remove crop debris', 'Strobilurin or triazole fungicides', 'Tillage to bury residue, resistant varieties, avoid dense planting'),
('Corn_(maize)___healthy', 'Corn', 'No disease detected', 'Leaf appears healthy with no visible symptoms', 'Continue regular care and monitoring', 'No treatment needed', 'Maintain proper fertilization and irrigation'),
('Grape___Black_rot', 'Grape', 'Fungus Guignardia bidwellii', 'Circular tan lesions with dark borders on leaves, shriveled berries', 'Sulfur spray, copper fungicide weekly', 'Myclobutanil or tebuconazole', 'Remove mummified grapes, prune for air flow, avoid overhead irrigation'),
('Grape___Esca_(Black_Measles)', 'Grape', 'Fungal complex (Phaeomoniella, Phaeoacremonium)', 'Tiger-stripe pattern on leaves, dark streaks in wood', 'Trichoderma application, pruning wound sealants', 'Fosetyl-Al or pyraclostrobin', 'Avoid pruning wounds in wet weather, maintain vine health'),
('Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape', 'Fungus Isariopsis clavispora', 'Dark brown irregular spots with yellow halos', 'Copper-based fungicide, neem oil', 'Mancozeb or iprodione fungicides', 'Proper canopy management, avoid leaf wetness'),
('Grape___healthy', 'Grape', 'No disease detected', 'Leaf appears healthy with no visible symptoms', 'Continue regular care and monitoring', 'No treatment needed', 'Maintain proper pruning and irrigation management'),
('Orange___Haunglongbing_(Citrus_greening)', 'Orange', 'Bacteria Candidatus Liberibacter asiaticus (spread by psyllid)', 'Yellow shoot, asymmetric blotchy mottling, stunted fruit', 'Remove infected trees, control psyllid with neem oil', 'Bactericides have limited effect; focus on vector control with insecticides', 'Remove infected trees immediately, control Asian citrus psyllid, use certified disease-free plants'),
('Peach___Bacterial_spot', 'Peach', 'Bacteria Xanthomonas campestris pv. pruni', 'Small, water-soaked spots on leaves, fruit cracking', 'Copper spray, compost tea, kaolin clay', 'Copper-based bactericides applied preventively', 'Resistant varieties, avoid overhead irrigation, proper pruning for airflow'),
('Peach___healthy', 'Peach', 'No disease detected', 'Leaf appears healthy with no visible symptoms', 'Continue regular care and monitoring', 'No treatment needed', 'Maintain proper pruning and pest monitoring'),
('Pepper,_bell___Bacterial_spot', 'Pepper', 'Bacteria Xanthomonas euvesicatoria', 'Water-soaked lesions turning brown with yellow halos', 'Copper spray, remove infected plant material', 'Copper hydroxide bactericides', 'Use disease-free seeds, avoid overhead irrigation, rotate crops'),
('Pepper,_bell___healthy', 'Pepper', 'No disease detected', 'Leaf appears healthy with no visible symptoms', 'Continue regular care and monitoring', 'No treatment needed', 'Maintain proper watering and nutrient management'),
('Potato___Early_blight', 'Potato', 'Fungus Alternaria solani', 'Dark brown target-like spots with concentric rings', 'Neem oil spray, baking soda solution, compost tea', 'Chlorothalonil or mancozeb applied every 7-10 days', 'Crop rotation (3+ years), remove infected plants, proper spacing'),
('Potato___Late_blight', 'Potato', 'Oomycete Phytophthora infestans', 'Water-soaked grayish-green lesions turning brown, white mold underneath', 'Copper spray, remove infected foliage immediately', 'Metalaxyl or chlorothalonil, apply preventively', 'Plant certified seed potatoes, good air circulation, avoid overhead watering'),
('Potato___healthy', 'Potato', 'No disease detected', 'Leaf appears healthy with no visible symptoms', 'Continue regular care and monitoring', 'No treatment needed', 'Maintain proper hilling and irrigation management'),
('Raspberry___healthy', 'Raspberry', 'No disease detected', 'Leaf appears healthy with no visible symptoms', 'Continue regular care and monitoring', 'No treatment needed', 'Maintain proper pruning of old canes'),
('Soybean___healthy', 'Soybean', 'No disease detected', 'Leaf appears healthy with no visible symptoms', 'Continue regular care and monitoring', 'No treatment needed', 'Maintain proper row spacing and weed management'),
('Squash___Powdery_mildew', 'Squash', 'Fungus Podosphaera xanthii', 'White powdery patches on upper leaf surface', 'Baking soda spray, milk solution, neem oil', 'Sulfur or trifloxystrobin fungicides', 'Plant resistant varieties, ensure good air circulation, avoid overhead watering'),
('Strawberry___Leaf_scorch', 'Strawberry', 'Fungus Diplocarpon earlianum', 'Small, purple spots enlarging with reddish-purple borders', 'Neem oil, copper fungicide, remove old leaves', 'Captan or myclobutanil fungicides', 'Remove infected leaves, avoid overhead irrigation, proper plant spacing'),
('Strawberry___healthy', 'Strawberry', 'No disease detected', 'Leaf appears healthy with no visible symptoms', 'Continue regular care and monitoring', 'No treatment needed', 'Maintain proper mulching and runner management'),
('Tomato___Bacterial_spot', 'Tomato', 'Bacteria Xanthomonas species', 'Small, water-soaked spots with yellow halos on leaves and fruit', 'Copper spray mixed with mancozeb, neem oil', 'Copper-based bactericides, streptomycin sulfate', 'Use disease-free seed, avoid overhead irrigation, 2-3 year crop rotation'),
('Tomato___Early_blight', 'Tomato', 'Fungus Alternaria solani', 'Dark spots with concentric rings (target board appearance)', 'Neem oil, baking soda spray, remove lower infected leaves', 'Chlorothalonil, mancozeb, or azoxystrobin', 'Mulch soil, avoid wetting foliage, remove infected leaves promptly'),
('Tomato___Late_blight', 'Tomato', 'Oomycete Phytophthora infestans', 'Greasy, water-soaked lesions turning brown-black', 'Copper fungicide spray, remove infected plants immediately', 'Metalaxyl, chlorothalonil applied preventively', 'Avoid overhead watering, ensure drainage, remove volunteer plants'),
('Tomato___Leaf_Mold', 'Tomato', 'Fungus Passalora fulva', 'Yellow spots on upper surface, olive-green mold below', 'Neem oil, increase ventilation, compost tea', 'Chlorothalonil or mancozeb', 'Improve greenhouse ventilation, avoid leaf wetness, resistant varieties'),
('Tomato___Septoria_leaf_spot', 'Tomato', 'Fungus Septoria lycopersici', 'Small circular spots with dark borders and light centers', 'Copper fungicide, neem oil, remove infected leaves', 'Chlorothalonil or mancozeb every 7-14 days', 'Mulch to prevent soil splash, remove lower leaves, crop rotation'),
('Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato', 'Mite Tetranychus urticae', 'Fine stippling on leaves, bronzing, tiny webs', 'Neem oil, insecticidal soap, predatory mites', 'Abamectin or bifenazate miticides', 'Increase humidity, remove infested leaves, avoid dusty conditions'),
('Tomato___Target_Spot', 'Tomato', 'Fungus Corynespora cassiicola', 'Dark brown spots with concentric rings and yellow halo', 'Neem oil spray, copper fungicide', 'Azoxystrobin or tebuconazole', 'Improve air circulation, avoid leaf wetness, remove infected debris'),
('Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato', 'Virus transmitted by whitefly (Bemisia tabaci)', 'Upward leaf curling, yellowing, stunted growth', 'Control whiteflies with neem oil, reflective mulch', 'Imidacloprid for whitefly control (vector management)', 'Use resistant varieties, yellow sticky traps, remove infected plants'),
('Tomato___Tomato_mosaic_virus', 'Tomato', 'Tobacco mosaic virus (TMV)', 'Mosaic pattern of light and dark green, leaf distortion', 'Remove infected plants, wash hands and tools, no cure', 'No effective chemical treatment; focus on prevention', 'Use resistant varieties, disinfect tools, avoid tobacco near plants'),
('Tomato___healthy', 'Tomato', 'No disease detected', 'Leaf appears healthy with no visible symptoms', 'Continue regular care and monitoring', 'No treatment needed', 'Maintain proper staking, pruning, and irrigation');
