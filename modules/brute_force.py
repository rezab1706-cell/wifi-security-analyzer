#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Brute Force Module
Performs dictionary and brute force attacks on WiFi networks
"""

import threading
import time
from typing import Optional, List, Dict
from pathlib import Path
import hashlib
import itertools
from config import BRUTE_FORCE_THREADS, COMMON_PASSWORDS

class BruteForce:
    def __init__(self):
        self.threads = BRUTE_FORCE_THREADS
        self.common_passwords = COMMON_PASSWORDS
        self.found_password = None
        self.is_running = False
        
    def dictionary_attack(self, ssid: str, wordlist_path: str = None) -> Optional[str]:
        """
        Perform dictionary attack using wordlist
        
        Args:
            ssid: Target WiFi SSID
            wordlist_path: Path to wordlist file
            
        Returns:
            Found password or None
        """
        if wordlist_path is None:
            wordlist = self.common_passwords
        else:
            try:
                with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                    wordlist = [line.strip() for line in f if line.strip()]
            except Exception as e:
                print(f"[!] Error reading wordlist: {str(e)}")
                return None
        
        print(f"[*] Starting dictionary attack on {ssid}")
        print(f"[*] Testing {len(wordlist)} passwords")
        
        self.is_running = True
        self.found_password = None
        
        # Split wordlist for multi-threaded attack
        chunk_size = len(wordlist) // self.threads
        threads = []
        
        for i in range(self.threads):
            start = i * chunk_size
            end = start + chunk_size if i < self.threads - 1 else len(wordlist)
            chunk = wordlist[start:end]
            
            thread = threading.Thread(
                target=self._test_passwords,
                args=(ssid, chunk, i)
            )
            threads.append(thread)
            thread.start()
        
        # Wait for threads to complete
        for thread in threads:
            thread.join()
        
        self.is_running = False
        return self.found_password
    
    def _test_passwords(self, ssid: str, passwords: List[str], thread_id: int) -> None:
        """
        Test passwords in a thread
        """
        for i, password in enumerate(passwords):
            if self.found_password or not self.is_running:
                break
            
            if self._try_password(ssid, password):
                self.found_password = password
                print(f"[+] PASSWORD FOUND: {password}")
                break
            
            # Progress indicator
            if (i + 1) % 100 == 0:
                print(f"[Thread {thread_id}] Tested {i + 1} passwords...")
    
    def _try_password(self, ssid: str, password: str) -> bool:
        """
        Test if password is correct
        This is a simplified version - actual implementation would
        connect to the network or use proper WPA2 verification
        """
        # Simulate password testing
        # In real implementation, this would use WPA2 key derivation
        return False
    
    def brute_force_attack(self, ssid: str, min_length: int = 1, max_length: int = 8,
                          charset: str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') -> Optional[str]:
        """
        Perform brute force attack with character set
        
        Args:
            ssid: Target WiFi SSID
            min_length: Minimum password length
            max_length: Maximum password length
            charset: Characters to use in brute force
            
        Returns:
            Found password or None
        """
        print(f"[*] Starting brute force attack on {ssid}")
        print(f"[*] Length range: {min_length}-{max_length}")
        
        self.is_running = True
        self.found_password = None
        
        for length in range(min_length, max_length + 1):
            total_combinations = len(charset) ** length
            print(f"[*] Testing length {length} ({total_combinations} combinations)")
            
            count = 0
            for combination in itertools.product(charset, repeat=length):
                if not self.is_running:
                    break
                
                password = ''.join(combination)
                
                if self._try_password(ssid, password):
                    self.found_password = password
                    print(f"[+] PASSWORD FOUND: {password}")
                    return password
                
                count += 1
                if count % 10000 == 0:
                    print(f"[*] Tested {count}/{total_combinations} combinations...")
            
            if self.found_password:
                break
        
        self.is_running = False
        return self.found_password
    
    def hybrid_attack(self, ssid: str, base_wordlist: List[str],
                     rules: List[str] = None) -> Optional[str]:
        """
        Perform hybrid attack (wordlist + rules)
        
        Args:
            ssid: Target WiFi SSID
            base_wordlist: Base wordlist
            rules: Mutation rules
            
        Returns:
            Found password or None
        """
        if rules is None:
            rules = ['', '123', '!', '@', '#', '2024']
        
        print(f"[*] Starting hybrid attack on {ssid}")
        
        hybrid_wordlist = []
        for word in base_wordlist:
            hybrid_wordlist.append(word)
            for rule in rules:
                hybrid_wordlist.append(word + rule)
        
        return self.dictionary_attack(ssid, wordlist=hybrid_wordlist)
    
    def stop_attack(self) -> None:
        """
        Stop ongoing attack
        """
        self.is_running = False
        print("[*] Attack stopped")
