clear all

%% 1. Lire les donnees avec csvread

data = csvread('profilgravi.dat');
%% Imprimer les dimensions
sprintf('Dimensions des donnees: %d x %d', size(data,1), size(data, 2))
%% 2. Définir vecteurs gravite et position
%%
posx = data(:,1)'
grav = data(:,2)'
%% 3. Tracer le signal original
%%
figure()
plot(posx, grav);
xlabel('Position (m)')
ylabel('Gravite (mGal)')
%% 4. Certaines definitions
%%
Fs = 1;            % Frequence d'echantillonnage                 
T = 1/Fs;          % Periodre d'echantillonnage  
L = length(data);  % Longueur du signal
%% 5. Calculer la transformee directe
%%
tfg = fftshift(fft(grav));
sprintf('Dimensions transformee: %d',length(tfg))
sprintf('Nombres reels?: %d',isreal(tfg))
%% 6. Définir le vecteur des frequences et visualiser la transformee
%%
dF = Fs/L;
freq = -Fs/2:dF:Fs/2-dF;
figure()
semilogy(freq, abs(tfg));
xlabel('Frequence spatiale (m^{-1})');
ylabel('Amplitude (mGal)')
%% 7. Couper les hautes frequences
%%
cut = abs(freq) > 0.01; % La valeur de coupure depend du signal
tfg(cut) = 0; % Remplacer les valeurs a couper par 0

% Imprimer le masque
cutoff = [freq; cut];
fprintf('%8.3f %8.0f\n', cutoff)
%% 8. Faire la transformee inverse du signal coupe
%%
grav_coupe = ifft(ifftshift(tfg));
%% 9. Faire un graphique avec les trois signaux
%%
figure()
hold on;
plot(posx, grav);
plot(posx, grav_coupe);
plot(posx, grav-grav_coupe);
legend('Profil original', 'Filtre passe-bas', 'Signal residuel')
xlabel('Position (m)')
ylabel('Gravite (mGal)')