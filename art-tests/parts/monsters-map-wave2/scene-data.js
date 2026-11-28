"use strict";

const Scenes = [
  { id: "crystal", name: "Hang pha lê", map: "hang1.png", actors: [
    { id: "bat", x: 429, y: 451, h: 76, face: 1, dx: 16, dy: 14 },
    { id: "spider", x: 490, y: 578, h: 87, face: -1, dx: 11, dy: 17 },
    { id: "spiderQueen", x: 735, y: 641, h: 155, face: 1, dx: 10, dy: 15 },
    { id: "spider", x: 908, y: 511, h: 88, face: 1, dx: 12, dy: -14 },
    { id: "bat", x: 1087, y: 757, h: 82, face: -1, dx: 13, dy: 16 },
    { id: "spider", x: 810, y: 918, h: 92, face: 1, dx: 10, dy: 13 }
  ] },
  { id: "ice", name: "Hang băng", map: "hang2.png", actors: [
    { id: "iceWolf", x: 280, y: 515, h: 97, face: 1, dx: 13, dy: -9 },
    { id: "iceWitch", x: 584, y: 586, h: 122, face: 1, dx: 12, dy: 8 },
    { id: "iceGolem", x: 839, y: 508, h: 158, face: 1, dx: 10, dy: 8 },
    { id: "iceWolf", x: 1001, y: 665, h: 104, face: -1, dx: 9, dy: 11 },
    { id: "iceWitch", x: 1154, y: 860, h: 117, face: -1, dx: 9, dy: 9 }
  ] },
  { id: "lava", name: "Hang dung nham", map: "hang3.png", actors: [
    { id: "imp", x: 329, y: 579, h: 95, face: 1, dx: 12, dy: 5 },
    { id: "magmaGolem", x: 623, y: 563, h: 153, face: -1, dx: 13, dy: 9 },
    { id: "imp", x: 608, y: 213, h: 95, face: -1, dx: 8, dy: 11 },
    { id: "magmaGolem", x: 984, y: 622, h: 150, face: 1, dx: 9, dy: 10 },
    { id: "imp", x: 840, y: 822, h: 94, face: 1, dx: 10, dy: 12 }
  ] },
  { id: "iceArena", name: "Đấu trường băng", map: "boss_bang.png", actors: [
    { id: "iceGolem", x: 702, y: 649, h: 246, face: 1, dx: 18, dy: 14 },
    { id: "iceWitch", x: 454, y: 635, h: 132, face: 1, dx: 13, dy: 6 },
    { id: "iceWolf", x: 959, y: 660, h: 113, face: -1, dx: 15, dy: -8 }
  ] },
  { id: "fireArena", name: "Đấu trường lửa", map: "bosslua.png", actors: [
    { id: "fireDragon", x: 702, y: 650, h: 255, face: 1, dx: 10, dy: 13 },
    { id: "magmaGolem", x: 963, y: 670, h: 160, face: -1, dx: 12, dy: 8 },
    { id: "imp", x: 449, y: 628, h: 108, face: 1, dx: 14, dy: 11 }
  ] },
];
