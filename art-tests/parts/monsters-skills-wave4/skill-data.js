"use strict";

const SkillScenes = [
  { id:"skeleton-slash", actor:"skeleton", title:"Xương Khô · Chém kiếm", event:"melee", mode:"melee", impact:"slash", hit:430, end:780, part:"arm_r_sword", amount:-55, hint:"Vệt chém đi theo đòn cận chiến." },
  { id:"lizard-claw", actor:"lizard", title:"Thằn Lằn Đầm · Cào", event:"melee", mode:"melee", impact:"slash", hit:360, end:660, part:"arm_l", amount:-36, hint:"Vung vuốt cận chiến." },
  { id:"scorpion-sting", actor:"scorpion", title:"Bọ Cạp Cát · Chích độc", event:"melee", mode:"melee", impact:"poison", hit:510, end:890, part:"tail", amount:35, hint:"Độc đi cùng cú chích cận chiến." },
  { id:"vulture-dive", actor:"vulture", title:"Kền Kền · Sà xuống", event:"melee", mode:"melee", impact:"slash", hit:540, end:880, part:"wing_l", amount:34, hint:"Dáng sà của đòn cận chiến khi bay." },
  { id:"yeti-punch", actor:"yeti", title:"Yêu Tuyết · Đấm nặng", event:"tank", mode:"melee", impact:"ice-hit", hit:520, end:920, part:"arm_l", amount:-38, hint:"Hiệu ứng tập trung ở mục tiêu cận chiến." },
  { id:"vampire-blood", actor:"vampire", title:"Ma Cà Rồng · Huyết cầu", event:"blood", mode:"projectile", projectile:"blood", impact:"blood", hit:790, release:350, end:1240, part:"arm_l_forearm", amount:-36, drain:true, hint:"Hồi máu cho quái nếu đạn gây sát thương." },
  { id:"spider-venom", actor:"spider", title:"Nhện Độc · Phun độc", event:"venom", mode:"projectile", projectile:"poison", impact:"poison", hit:770, release:310, end:1060, hint:"Đạn độc của Nhện Độc và Cóc Độc." },
  { id:"imp-fire", actor:"imp", title:"Hỏa Ma · Cầu lửa", event:"fire", mode:"projectile", projectile:"fire", impact:"nova", hit:720, release:330, end:1050, hint:"Đạn lửa bay theo hướng đã nhắm." },
  { id:"iceWitch-frost", actor:"iceWitch", title:"Phù Thủy Băng · Đạn băng", event:"frost", mode:"projectile", projectile:"frost", impact:"ice-hit", hit:800, release:360, end:1130, hint:"Đạn băng mang hiệu ứng làm chậm." },
  { id:"wraith-magic", actor:"wraith", title:"Hồn Ma · Đạn bóng", event:"magic", mode:"projectile", projectile:"magic", impact:"magic", hit:790, release:330, end:1120, hint:"Đạn phép của Hồn Ma." },
  { id:"goblin-arrow", actor:"goblinArcher", title:"Goblin Cung Thủ · Bắn tên", event:"arrow", mode:"projectile", projectile:"arrow", impact:"slash", hit:670, release:310, end:960, hint:"Tên xoay theo hướng bay." },
  { id:"shaman-heal", actor:"goblinShaman", title:"Pháp Sư Goblin · Hồi máu", event:"healer", mode:"support", impact:"heal", hit:420, end:1120, ally:"goblin", hint:"Vòng hồi máu đặt dưới chân đồng minh." },
  { id:"dragon-nova", actor:"fireDragon", title:"Rồng Lửa · Nổ diện rộng", event:"nova", mode:"circle", impact:"nova", warn:900, hit:900, end:1390, hint:"Hiện vòng báo đòn 0,9 giây theo game." },
  { id:"wolf-howl", actor:"wolfLord", title:"Chúa Sói · Gầm choáng", event:"howl", mode:"circle", impact:"magic", warn:900, hit:900, end:1390, hint:"Hiện vòng báo đòn 0,9 giây theo game." },
  { id:"wolf-charge", actor:"wolfLord", title:"Chúa Sói · Lao húc", event:"charge", mode:"line", impact:"slash", warn:700, hit:700, end:1250, hint:"Hiện vệt báo hướng lao 0,7 giây theo game." },
  { id:"pharaoh-summon", actor:"pharaoh", title:"Pharaoh · Triệu hồi", event:"summon", mode:"support", impact:"summon", hit:460, end:1220, summon:"mummy", hint:"Hiệu ứng đặt tại vị trí quái được triệu hồi." }
];
