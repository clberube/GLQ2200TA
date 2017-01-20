% Importer les données du TP03
data = csvread('Donnees_gravite_TP03.csv');
% Séparer les colonnes
axeX = data(:,1);
g = data(:,2);
figure();
plot(axeX/100, 1000*g, 'k.');

% On sait que:
    % Roche encaissante:
            % Densite 2.67 g/cm3
    % Corps 1:
            % Densite INCONNUE
            % Rayon 12.8 m
            % Profondeur 19.0 m
    % Corps 2:
            % Densite 1.00 g/cm3
            % Rayon INCONNU
            % Profondeur 23.0 m
    % Corps 3:
            % Densite 0.00 g/cm3
            % Rayon 10 m
            % Profondeur INCONNUE

% Générer des listes vides pour entreposer les paramètres 
% qui seront acceptés 
rho_corps1 = zeros();
R_corps2 = zeros();
z_corps3 = zeros();
RMS_list = zeros();

% Inversion Monte Carlo
% Tester N hypothèses et calculer la fonction objectif
c = 0; % Compteur à 0
for i = 1:10000
    % Générer des paramètres de façon aléatoire
    rho_hypothese = unifrnd(0,10);
    R_hypothese = unifrnd(0,23)*100;
    z_hypothese = unifrnd(10,50)*100;
    % Calculer le modèle proposé
    g_model = grav_sphere(axeX, rho_hypothese, 12.8*100, 75*100, 19*100) + grav_sphere(axeX, -1.67, R_hypothese, 200*100, 23*100) + grav_cylindre(axeX, -2.67, 10.0*100, 350*100, z_hypothese);
    % La fonction objectif (Root Mean Square Error)
    RMS = sqrt(mean((g_model - g).^2));
    % Entreposer les paramètres si c'est la première itération ou si la 
    % nouvelle hypothèse est meilleure que la précédente
    if (i == 1) || (RMS < RMS_list(end))
        c = c+1; % Faire monter le compteur 
        RMS_list(c) = RMS;
        rho_corps1(c) = rho_hypothese;
        R_corps2(c) = R_hypothese;
        z_corps3(c) = z_hypothese;
    end
end

% Tracer le graphique du meilleur modèle
best_g = grav_sphere(axeX, rho_corps1(end), 12.8*100, 75*100, 19*100) + grav_sphere(axeX, -1.67, R_corps2(end), 200*100, 23*100) + grav_cylindre(axeX, -2.67, 10.0*100, 350*100, z_corps3(end));
figure();
hold on;
plot(axeX/100, 1000*g, 'k.');
plot(axeX/100, 1000*best_g, 'r-', 'Linewidth',2);
hold off;
xlabel('Position');
ylabel('mGal');
figure();
plot(RMS_list);
sprintf('Densité du corps 1: %.3f g/cc', rho_corps1(end)) 
sprintf('Rayon du corps 2: %.3f m', R_corps2(end)/100)
sprintf('Profondeur du corps 3: %.3f m', z_corps3(end)/100)
