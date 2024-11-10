import UIKit

class CatImageViewController: UIViewController {
    @IBOutlet weak var catNameLabel: UILabel!
    @IBOutlet weak var imageView: UIImageView!
    
    var catName: String?
    var catImage: UIImage?
    
    override func viewDidLoad() {
        super.viewDidLoad()

        catNameLabel.text = catName
        imageView.image = catImage
        imageView.contentMode = .scaleToFill
        imageView.layer.cornerRadius = 30
    }

}
