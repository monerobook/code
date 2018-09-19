// main.cpp file for Tutorial 5 - Mastering Monero

#include "cryptonote_core/blockchain.h"
#include "common/base58.h"
#include "crypto/crypto-ops.h"
#include "crypto/hash.h"

// Converts crypto::hash into crypto::secret_key or crypto::public_key
template <typename T>
T get_key_from_hash(crypto::hash & in_hash){
	T* key;
	key = reinterpret_cast<T*>(&in_hash);
	return *key;
}

int main(){
  	// Put here your private spendable key!
	std::string str_spend_key = "f8f2fba1da00643bbf11ffec355a808d2d8ca4e4de14a10476e116abd8dd7f02";
	cryptonote::network_type nettype = cryptonote::MAINNET;	
	crypto::public_key public_spend_key;

	// Convert hex string to binary data
	cryptonote::blobdata blob;
	epee::string_tools::parse_hexstr_to_binbuff(str_spend_key, blob);
	crypto::secret_key sc = *reinterpret_cast<const crypto::secret_key *>(blob.data());
	std::cout << "Private spend key : " << sc << std::endl;

	// Generate public spend key based on the private spend key (sc)
	crypto::secret_key_to_public_key(sc, public_spend_key);
	
	std::cout << "Public spend key : "  << public_spend_key  << std::endl;
	
	crypto::hash hash_of_private_spend_key;
	
	crypto::cn_fast_hash(&sc, sizeof(hash_of_private_spend_key), hash_of_private_spend_key);

	crypto::secret_key private_view_key;
	crypto::public_key public_view_key;
	
	crypto::generate_keys(public_view_key,private_view_key,get_key_from_hash<crypto::secret_key>(hash_of_private_spend_key), true);
	
	std::cout << "\n" << "Private view key : "  << private_view_key << std::endl;
	std::cout << "Public view key  : "  << public_view_key  << std::endl;
  

	cryptonote::account_public_address address {public_spend_key, public_view_key};
	std::string public_address;

	public_address = cryptonote::get_account_address_as_str(nettype, false, address); 
	std::cout << "Monero Address:" << public_address << std::endl;

	return 0;
}
