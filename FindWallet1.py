from mnemonic import Mnemonic
from unidecode import unidecode
from constants import LENGTH_STRENGTH, LANGUAGES
import bip32utils
import wallets

# Pesquisa por endereços em uma lista, gerados a partir das frases para recuperar usadas para recuperar a carteira.
# As frases são geradas aleatoriamente.

def mnemonic(phrase, count):

	try:

		mnemon = Mnemonic('english')
		#words = mnemon.generate(256)
		#print(words)
		#mnemon.check(words)
		#seed = mnemon.to_seed(words)
		seed = mnemon.to_seed(phrase)
		
		root_key = bip32utils.BIP32Key.fromEntropy(seed)
		#root_key.dump()
		root_address = root_key.Address()
		root_public_hex = root_key.PublicKey().hex()
		root_private_wif = root_key.WalletImportFormat()
		
		child_key = root_key.ChildKey(0).ChildKey(0)
		child_address = child_key.Address()
		child_public_hex = child_key.PublicKey().hex()
		child_private_wif = child_key.WalletImportFormat()

		if ((root_address in wallets.wallets) or (child_address in wallets.wallets)):
			arquivo = open(f"Phrase{count}.txt", "a")

			arquivo.write(f"\nRoot key:\n\nPhrase: {phrase}\nAddress: {root_address}\nPublic : {root_public_hex}\nPrivate: {root_private_wif}\n\nChild key m/0/0:\n\nAddress: {child_address}\nPublic : {child_public_hex}\nPrivate: {child_private_wif}")

			arquivo.close()

			print(f"\n\nEncontrado na tentativa: {count}")

			print(f'\n\nBIP39 Seed: {seed.hex()}\n\n')

			print('Root key:')
			print(F"\nPhrase: {phrase}")
			print(f'\tAddress: {root_address}')
			print(f'\tPublic : {root_public_hex}')
			print(f'\tPrivate: {root_private_wif}\n')

			print('Child key m/0/0:')
			print(f'\tAddress: {child_address}')
			print(f'\tPublic : {child_public_hex}')
			print(f'\tPrivate: {child_private_wif}\n')	

		else:
			print(f"\n{count}: Endereço: {root_address} não encontrado na lista.")
			print(f"\n{count}: Endereço: {child_address} não encontrado na lista.")

		return True

	except Exception as error:
		print(f"\n\nError: {error}")

		return False

def strength(length: int) -> int:
    strength = LENGTH_STRENGTH[length]
    return strength


def generate_seed(strength: int, lang: str) -> str:
    mnemo = Mnemonic(LANGUAGES[lang])

    seed_phrase = mnemo.generate(strength=strength)
    seed_list = seed_phrase.split()
    final_seed_list = [unidecode(word) for word in seed_list]
    final_seed_phrase = " ".join(final_seed_list)

    return final_seed_phrase

def main():

	try:
		strength1 = strength(12)
		#mnemonic(b'lucky labor rally law toss orange weasel try surge meadow type crumble proud slide century')
		for i in range(0, 1000000):
			mnemonic(generate_seed(strength1, 'en'), i)

		return True

	except Exception as error:
		print(f"\n\nError: {error}")

		return False

if (__name__ == '__main__'):
	main()

