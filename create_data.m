% Axe des X et paramètres intiaux pour calculer la réponse des corps simples
axeX = 100*(0:500);

rho_1 = 3.78;
R_1 = 12.8*100;
PosX_1 = 75*100;
PosZ_1 = 19*100;

rho_2 = -1.67;
R_2 = 16.3*100;
PosX_2 = 200*100;
PosZ_2 = 23*100;

rho_3 = -2.67;
R_3 = 10.0*100;
PosX_3 = 350*100;
PosZ_3 = 21.5*100;

% Générer le data synthétique à partir des paramètres initiaux
g_1 = grav_sphere(axeX, rho_1, R_1, PosX_1, PosZ_1);
g_2 = grav_sphere(axeX, rho_2, R_2, PosX_2, PosZ_2);
g_3 = grav_cylindre(axeX, rho_3, R_3, PosX_3, PosZ_3);
g_data = g_1 + g_2 + g_3;
% Ajouter un bruit Gaussien de 2%
g_data = g_data + normrnd(0,0.02*max(abs(g_data)), 1, length(g_data));
csvwrite('Donnees_gravite_TP03.csv',[axeX; g_data]')