from collections import defaultdict
import math
import numpy as np
import time
import threading
from assets import load_experiments, load_particles, load_user_data, save_user_data

class ProductionManager:
    def __init__(self):
        self.rng = np.random.default_rng()
        self.stop_signal = threading.Event()

        # Carregamento inicial dos dados
        self.experiments = load_experiments()
        self.particles = load_particles()["particles"]
        self.user_data = load_user_data()

        # Estado do jogo
        self.prod_multiplier = 0  # Pode ser modificado por upgrades depois

        # Dicionários principais
        self.decay_buffer = defaultdict(float)
        self.production = defaultdict(float)            # produção por segundo
        self.products = defaultdict(float)              # partículas em produção contínua
        self.whole_products = defaultdict(int)          # contador de unidades inteiras
        self.particles_produced_tick = defaultdict(float)  # tempo total para gerar cada partícula

    def stop(self):
        self.stop_signal.set()

    def recalculate(self):
        self.production.clear()
        self.particles_produced_tick.clear()

        experiments_tick = 0
        for name, item in self.experiments.items():
            if name in self.user_data["experiments"]:
                experiments_tick += item["tick"]
                for product in item.get("subproducts", []):
                    self.particles_produced_tick[product] = 0

        for name, pdata in self.particles.items():
            if name in self.particles_produced_tick:
                self.particles_produced_tick[name] = pdata["production_time_game_sec"] * experiments_tick

        for name, ptime in self.particles_produced_tick.items():
            self.production[name] = 1 / ptime if ptime > 0 else 0

    def update_particles_inventory(self):
        confirm_user_data = load_user_data()
        for name in self.particles:
            saved_qty = confirm_user_data.get(name, 0)
            if saved_qty > 0:
                self.products[name] = float(saved_qty)


    def tick(self):
        for name, rate in self.production.items():
            self.products[name] += rate
        

    def register_production(self):
        for item, qty in self.products.items():
            int_qty = math.floor(qty)
            self.user_data[item] = int_qty
            save_user_data(self.user_data)

    def tick_autoloop(self, interval=0.25):
        self.update_particles_inventory()
        while not self.stop_signal.is_set():
            for name, rate in self.production.items():
                self.products[name] += rate
            self.decay_particles()
            time.sleep(interval)
        

    def register_production_autoloop(self, interval=10):
        while not self.stop_signal.is_set():
            for item, qty in self.products.items():
                int_qty = math.floor(qty)
                self.user_data[item] = int_qty
            save_user_data(self.user_data)
            time.sleep(interval)


    def decay_particles(self, interval=0.25):
        for name, pdata in self.particles.items():
            if self.products.get(name, 0) < 1:
                continue

            lifetime = pdata.get("lifetime_game_sec", 0)
            if lifetime <= 0:
                continue

            decay_amount = self.products[name] * (interval / lifetime)
            self.decay_buffer[name] += decay_amount

            while self.decay_buffer[name] >= 1:
                self.products[name] -= 1
                self.decay_buffer[name] -= 1

                if self.products[name] < 0:
                    self.products[name] = 0
                    self.decay_buffer[name] = 0  # limpa também
